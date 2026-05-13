# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

Ansible playbook that provisions a Kali Linux workstation (locally or over SSH) with system tweaks, dev tools, terminal/desktop customisation, and security testing tooling. Designed to be run repeatedly — tasks should be idempotent.

## Common commands

```bash
# Run the full playbook against localhost (default inventory target)
ansible-playbook site.yaml

# Run a specific role or task by tag (see README.md for the full tag list)
ansible-playbook site.yaml -t tools
ansible-playbook site.yaml -t rust,python

# Run against a remote host defined in inventory/hosts.yaml
ansible-playbook site.yaml --limit kali-target -t tools

# Lint (same command CI runs in .github/workflows/lint.yaml)
ansible-lint
```

`ansible.cfg` sets `ask_pass=True` and `become_ask_pass=True`, so every run prompts for SSH and sudo passwords. Output is appended to `ansible.log` (gitignored).

## Architecture

`site.yaml` runs five roles in order against `hosts: all`, each gated by a tag matching the role name: **system → ssh → tools → terminal → desktop**. The default inventory targets `localhost` via `ansible_connection: local`; a commented `remote` group in `inventory/hosts.yaml` is the template for SSH targets.

Each role follows the same shape:

- `roles/<role>/tasks/main.yaml` is a dispatcher: it `import_tasks`-includes one sub-task file per logical chunk, and each import is tagged. For example, `roles/tools/tasks/main.yaml` imports `apt.yaml`, `rust.yaml`, `python.yaml`, … each with its own tag (`apt`, `rust`, `python`, …). This is what lets `-t rust,python` work without running the rest of the role.
- `roles/<role>/files/` holds static assets copied to the target (configs, scripts, the bundled Obsidian vault, etc.). `roles/<role>/templates/` holds Jinja-rendered files (e.g. `binaryninja.desktop`).
- There are no `defaults/` or `vars/` directories — facts are computed inline with `set_fact` when needed (e.g. fetching the latest Obsidian release tag from GitHub before installing).

Conventions to preserve when editing:

- **Variable namespacing**: registered vars and facts are prefixed with the role name (`tools_obsidian_version`, `desktop_panel_plugin_ids`, `tools_rockyou_gz`). Keep this pattern when adding new vars so cross-role collisions stay impossible.
- **Per-task `become`**: `become: true` is set on individual tasks that need root, not on the role or play. Don't blanket-elevate.
- **Home directory references**: use `{{ ansible_facts['env']['HOME'] }}` (not `~` or `lookup('env', 'HOME')`) — this is what every existing task uses and it resolves correctly under `become`.
- **APT third-party repos**: the pattern in `roles/tools/tasks/apt.yaml` is `get_url` the ASCII key → `gpg --dearmor` it into `/usr/share/keyrings/` or `/etc/apt/keyrings/` → register the repo with `ansible.builtin.deb822_repository`. Follow this when adding new third-party APT sources rather than using `apt_key` (deprecated) or inline `apt-key add`.
- **Idempotent shell-outs**: when a task can't be expressed with a module (e.g. `gpg --dearmor`, running an installer script), guard it with `creates:` or a preceding `stat` + `when:` so re-runs are no-ops. See the `uv` install block in `roles/tools/tasks/python.yaml` for the stat-then-when pattern.
- **`.zshrc` edits** use `blockinfile` with a unique `marker` per block (`# {mark} ANSIBLE MANAGED BLOCK - <name>`) so each managed block can be updated/removed independently.

## Tags

Tags are the primary UX. The top-level role tag (`system`, `tools`, …) runs the whole role; each imported sub-task file adds a finer-grained tag. When adding a new sub-task file, add it to the role's `main.yaml` with both `import_tasks:` and `tags:` so it's reachable individually. The README "Available Tags" table should be kept in sync.

## Linting

`ansible-lint` runs in CI with `profile: production` and skips only `package-latest` (intentional, system upgrades) and `no-handler` (one-shot setup, no handlers). New code is expected to pass at production profile without adding to the skip list.
