"""Parse nmap normal-format output (-oN) into a markdown report.

One code block per up host, plus a code block for the originating command(s).

Usage:
    python nmap_to_md.py <nmap_output> [<nmap_output> ...] [-o report.md]
    cat scan.nmap | python nmap_to_md.py -
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


# ---------- Data model ----------

@dataclass
class Port:
    """A single open port row from an nmap scan."""
    port: int
    proto: str
    state: str
    service: str
    version: str = ""

    @property
    def spec(self) -> str:
        return f"{self.port}/{self.proto}"


@dataclass
class Host:
    """A single host block from an nmap scan."""
    ip: str
    hostname: str | None = None
    lines: list[str] = field(default_factory=list)
    ports: list[Port] = field(default_factory=list)

    @property
    def title(self) -> str:
        return f"{self.ip} ({self.hostname})" if self.hostname else self.ip

    @property
    def body(self) -> str:
        return "\n".join(self.lines).rstrip()


@dataclass
class NmapReport:
    command: str | None
    hosts: list[Host]
    down: list[str]


# ---------- Parsing ----------

# "Nmap scan report for HOSTNAME (IP)" or "Nmap scan report for IP".
# IP matches IPv4 dotted-quad or IPv6 (any hex/colon string, including ::).
_IP = r"[0-9A-Fa-f:.]+"
_REPORT_RE = re.compile(
    rf"^Nmap scan report for "
    rf"(?:(?P<host>[^\s()]+) \((?P<ip1>{_IP})\)|(?P<ip2>{_IP}))"
    r"(?:\s+\[(?P<status>host down)\])?\s*$"
)
_COMMAND_RE = re.compile(r"^# Nmap [^ ]+ scan initiated .*? as: (?P<cmd>.+?)\s*$")

# "1433/tcp  open  ms-sql-s  Microsoft SQL Server 2022 ..."
# State must be open/open|filtered to land in the summary; closed/filtered are skipped.
_PORT_RE = re.compile(
    r"^(?P<port>\d+)/(?P<proto>tcp|udp)\s+"
    r"(?P<state>open(?:\|filtered)?)\s+"
    r"(?P<service>\S+)"
    r"(?:\s+(?P<version>.+?))?\s*$"
)


def parse(text: str) -> NmapReport:
    """Parse an nmap -oN text blob into structured hosts."""
    command: str | None = None
    hosts: list[Host] = []
    down: list[str] = []
    current: Host | None = None

    for raw in text.splitlines():
        # Capture the initiating command line.
        if command is None:
            m = _COMMAND_RE.match(raw)
            if m:
                command = m.group("cmd").strip()
                continue

        m = _REPORT_RE.match(raw)
        if m:
            # New host begins — flush current and reset.
            if current is not None:
                hosts.append(current)
                current = None

            ip = m.group("ip1") or m.group("ip2")
            hostname = m.group("host")

            if m.group("status") == "host down":
                down.append(ip)
                continue  # don't start a host block for down hosts

            current = Host(ip=ip, hostname=hostname, lines=[raw])
            continue

        # Footer noise from nmap; stop collecting if we hit it mid-host.
        if raw.startswith("# Nmap done"):
            if current is not None:
                hosts.append(current)
                current = None
            break

        if current is not None:
            current.lines.append(raw)
            pm = _PORT_RE.match(raw)
            if pm:
                current.ports.append(Port(
                    port=int(pm.group("port")),
                    proto=pm.group("proto"),
                    state=pm.group("state"),
                    service=pm.group("service"),
                    version=(pm.group("version") or "").strip(),
                ))

    if current is not None:
        hosts.append(current)

    return NmapReport(command=command, hosts=hosts, down=down)


def merge(reports: list[NmapReport]) -> NmapReport:
    """Combine multiple parsed reports into one.

    Commands are joined with newlines so each source scan is visible.
    Hosts and down-lists are concatenated in order; deduplication is left
    to the caller since the same IP across files may have different findings.
    """
    if not reports:
        return NmapReport(command=None, hosts=[], down=[])
    if len(reports) == 1:
        return reports[0]

    commands = [r.command for r in reports if r.command]
    return NmapReport(
        command="\n".join(commands) if commands else None,
        hosts=[h for r in reports for h in r.hosts],
        down=[ip for r in reports for ip in r.down],
    )


# ---------- Rendering ----------

def _md_escape(text: str) -> str:
    """Escape pipe and backtick so they don't break table cells."""
    return text.replace("|", "\\|").replace("`", "\\`")


def _summary_table(hosts: list[Host]) -> list[str]:
    """Render a markdown table: one row per host with its open ports."""
    rows = ["| Checked | Host | Hostname | Open ports |", "|---|---|---|---|"]
    for h in hosts:
        ports = ", ".join(p.spec for p in h.ports) if h.ports else "—"
        rows.append(f"| [ ] | {h.ip} | {h.hostname or '—'} | {_md_escape(ports)} |")
    return rows


def render(report: NmapReport) -> str:
    parts: list[str] = []

    if report.command:
        parts += [
            "## Command",
            '```shell fold ln=false title="nmap command"',
            report.command,
            "```",
            "",
        ]

    if report.hosts:
        parts += ["## Summary", *_summary_table(report.hosts), ""]

    parts += [f"## Hosts ({len(report.hosts)} up, {len(report.down)} down)", ""]

    for host in report.hosts:
        parts += [
            f'```shell fold ln=false title="{host.title}"',
            host.body,
            "```",
            "",
        ]

    if report.down:
        parts += ["## Down hosts", *(f"- {ip}" for ip in report.down), ""]

    return "\n".join(parts).rstrip() + "\n"


# ---------- CLI ----------

def _read(source: str) -> str:
    if source == "-":
        return sys.stdin.read()
    return Path(source).read_text(encoding="utf-8", errors="replace")


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "inputs",
        nargs="+",
        help="one or more nmap -oN output files, or '-' for stdin",
    )
    parser.add_argument("-o", "--output", help="markdown file to write (default: stdout)")
    args = parser.parse_args(list(argv) if argv is not None else None)

    report = merge([parse(_read(src)) for src in args.inputs])
    md = render(report)

    if args.output:
        Path(args.output).write_text(md, encoding="utf-8")
    else:
        sys.stdout.write(md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
