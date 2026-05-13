#!/usr/bin/env python3
"""
ssh-audit output parser.

Parses ssh-audit text output and prints, for each of three categories:

  - key exchange algorithms                (kex)
  - encryption algorithms                  (enc)
  - message authentication code algorithms (mac)

a deduplicated bullet-point list of every algorithm that had at least
one [fail] or [warn] across any scanned host.  Fail/warn is not
differentiated and the reason text is not included.

After the algorithm lists, the script prints the set of hosts that had
at least one fail/warn anywhere.

Input formats accepted:
  - Single-host output (ssh-audit <host>), with (gen) target: header
    blocks and optional '------' separators between hosts.
  - Multi-target output (ssh-audit -T hosts.txt), where every line is
    prefixed with "host[:port] -- ".
  - Either of the above with ANSI color escape sequences embedded
    (stripped automatically).

Host address forms recognised in -T output:
  - hostname or IPv4, with optional :port           (host.example.com:2222)
  - bracketed IPv6, with optional :port             ([2001:db8::1]:8022)
  - bare IPv6 literal (no port, per ssh-audit's     (2001:db8::1)
    own convention requiring brackets when a
    port is specified)

Non-standard ports are preserved in the output; the full "host:port"
string is treated as the host identity, so the same address on different
ports is listed separately.

Usage:
    python3 ssh_audit_parser.py <ssh_audit_output_file> [...]
    cat output.txt | python3 ssh_audit_parser.py -
    ssh-audit -T hosts.all | python3 ssh_audit_parser.py -
"""

from __future__ import annotations

import re
import sys


# Strip ANSI color escape sequences (ssh-audit emits these by default when
# stdout is a TTY, but in some shells / wrappers they leak into pipes too).
ANSI_RE = re.compile(r"\x1B\[[0-9;]*[A-Za-z]")

# When ssh-audit is run with -T/--targets it produces a different layout: every
# line is prefixed with "host[:port] -- " and there are no "(gen) target:"
# blocks or "------" host separators.  Match and strip that prefix, capturing
# the target so we can track per-host context.
#
# Address forms accepted:
#   - bracketed IPv6 with optional port:   [2001:db8::1]:22  or  [2001:db8::1]
#   - bare IPv6 literal (no port — ambiguous with port form):  2001:db8::1
#   - hostname or IPv4 with optional port: example.com:22, 10.0.0.1:22, 10.0.0.1
#
# ssh-audit itself requires brackets around IPv6 literals when a port is
# present, so the bare-IPv6 case is only safe to match when no port follows.
TARGETS_PREFIX_RE = re.compile(
    r"""
    ^
    (?P<target>
        \[[0-9a-fA-F:]+\](?::\d+)?         # bracketed IPv6, optional :port
        |
        (?:[0-9a-fA-F]*:){2,}[0-9a-fA-F]+  # bare IPv6 (>=2 colons, no port)
        |
        [^\s:]+(?::\d+)?                   # hostname / IPv4, optional :port
    )
    \s+--\s+
    """,
    re.VERBOSE,
)

# Top-level "(xxx) name -- [sev] msg" line, where the [sev] portion is optional.
TOP_LINE_RE = re.compile(
    r"""
    ^\(
        (?P<cat>gen|kex|key|enc|mac|fin|rec|nfo)
    \)\s+
    (?P<name>.+?)
    (?:\s+--\s+\[(?P<sev>fail|warn|info)\]\s+.*)?
    \s*$
    """,
    re.VERBOSE,
)

# Continuation line: "`- [sev] msg" attached to the previous top-level entry.
CONT_LINE_RE = re.compile(r"""^\s*`-\s+\[(?P<sev>fail|warn|info)\]\s+""")

HOST_SEP_RE = re.compile(r"^-{5,}\s*$")

CATEGORY_LABEL = {
    "kex": "key exchange algorithms",
    "enc": "encryption algorithms",
    "mac": "message authentication code algorithms",
}


def parse(text: str):
    """
    Walk the raw output once and return:
        problem_algos: {category_code: ordered list of algorithm names}
        problem_hosts: ordered list of host targets with >=1 fail/warn
    Ordering preserves first-seen.
    """
    problem_algos = {"kex": [], "enc": [], "mac": []}
    seen_algo = {"kex": set(), "enc": set(), "mac": set()}

    problem_hosts: list[str] = []
    seen_host: set[str] = set()

    current_target: str | None = None
    # The most recent top-level entry, so continuation lines (`- [...])
    # attach to the right algorithm.
    last_cat: str | None = None
    last_name: str | None = None

    def flag(cat: str, name: str):
        """Record this algorithm and this host as having an issue."""
        if cat in problem_algos and name not in seen_algo[cat]:
            seen_algo[cat].add(name)
            problem_algos[cat].append(name)
        if current_target and current_target not in seen_host:
            seen_host.add(current_target)
            problem_hosts.append(current_target)

    for raw in text.splitlines():
        # Strip ANSI escapes that ssh-audit emits in colored output.
        line = ANSI_RE.sub("", raw).rstrip()
        if not line.strip():
            continue

        # When running with -T/--targets, each line is prefixed with
        # "host[:port] -- ".  Strip the prefix and treat the host as the
        # current target.  In -T mode there are no "(gen) target:" or
        # "------" separators, so this is our only signal.
        m_pfx = TARGETS_PREFIX_RE.match(line)
        if m_pfx:
            new_target = m_pfx.group("target")
            if new_target != current_target:
                # Host context switched — reset continuation tracking so a
                # `- continuation can't attach across hosts.
                last_cat = last_name = None
                current_target = new_target
            line = line[m_pfx.end():]

        if HOST_SEP_RE.match(line):
            last_cat = last_name = None
            current_target = None
            continue

        # Continuation line — attaches to the most recent top-level entry.
        m_cont = CONT_LINE_RE.match(line)
        if m_cont:
            sev = m_cont.group("sev")
            if (sev in ("fail", "warn")
                    and last_cat in problem_algos
                    and last_name):
                flag(last_cat, last_name)
            continue

        m = TOP_LINE_RE.match(line)
        if not m:
            continue

        cat = m.group("cat")
        name = m.group("name").strip()
        sev = m.group("sev")

        # Track the host target from the (gen) block.
        if cat == "gen":
            if ":" in name:
                key, _, value = name.partition(":")
                if key.strip().lower() == "target":
                    current_target = value.strip()
            last_cat = last_name = None
            continue

        # Remember this entry so continuation lines can find it, even for
        # categories we don't report on — that way stray `- lines under,
        # say, a (key) entry don't get misattributed to the previous (kex).
        last_cat, last_name = cat, name

        if cat in problem_algos and sev in ("fail", "warn"):
            flag(cat, name)

    return problem_algos, problem_hosts


def render(problem_algos, problem_hosts) -> str:
    out: list[str] = []
    for code in ("kex", "enc", "mac"):
        out.append(f"{CATEGORY_LABEL[code]}:")
        names = problem_algos[code]
        if names:
            for n in names:
                out.append(f"- {n}")
        else:
            out.append("  (none)")
        out.append("")

    out.append("hosts with at least one warning or failure:")
    if problem_hosts:
        for h in problem_hosts:
            out.append(f"- {h}")
    else:
        out.append("  (none)")
    return "\n".join(out) + "\n"


def _read_inputs(argv: list[str]) -> str:
    if not argv:
        sys.stderr.write(__doc__)
        sys.exit(2)
    chunks: list[str] = []
    for path in argv:
        if path == "-":
            chunks.append(sys.stdin.read())
        else:
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                chunks.append(fh.read())
    # Use the same divider the parser recognises so multiple files behave
    # as if concatenated.
    return ("\n" + "-" * 80 + "\n").join(chunks)


def main(argv: list[str]) -> int:
    text = _read_inputs(argv)
    problem_algos, problem_hosts = parse(text)
    sys.stdout.write(render(problem_algos, problem_hosts))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
