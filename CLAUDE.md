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

`ansible.cfg` sets `become_ask_pass = True`, so every run prompts for the sudo password. SSH passwords are not prompted for by default — the usual target is `localhost` over the `local` connection, where there is no SSH login; remote runs pass `-k`. Output is appended to `ansible.log` (gitignored).

## Architecture

`site.yaml` runs five roles in order against `hosts: all`, each gated by a tag matching the role name: **system → ssh → tools → terminal → desktop**. The default inventory targets `localhost` via `ansible_connection: local`; a commented `remote` group in `inventory/hosts.yaml` is the template for SSH targets.

Each role follows the same shape:

- `roles/<role>/tasks/main.yaml` is a dispatcher: it `import_tasks`-includes one sub-task file per logical chunk, and each import is tagged. For example, `roles/tools/tasks/main.yaml` imports `apt.yaml`, `rust.yaml`, `python.yaml`, … each with its own tag (`apt`, `rust`, `python`, …). This is what lets `-t rust,python` work without running the rest of the role.
- `roles/<role>/files/` holds static assets copied to the target (configs, scripts, the bundled Obsidian vault, etc.). `roles/<role>/templates/` holds Jinja-rendered files (e.g. `binaryninja.desktop`).
- `roles/<role>/defaults/main.yaml` holds the *what*: package lists, the repo clone list, the taskbar launcher list, regional settings. Task files hold the *how*. When adding a tool to an existing list, edit `defaults/`, not the task. Values only knowable at runtime (a latest release tag, a panel's current plugin IDs) are still computed inline with `set_fact` in the task file that uses them. There are no `vars/` directories.

Conventions to preserve when editing:

- **Variable namespacing**: registered vars and facts are prefixed with the role name (`tools_obsidian_version`, `desktop_panel_plugin_ids`, `tools_rockyou_gz`). Keep this pattern when adding new vars so cross-role collisions stay impossible.
- **Per-task `become`**: `become: true` is set on individual tasks that need root, not on the role or play. Don't blanket-elevate.
- **Home directory references**: use `{{ ansible_facts['env']['HOME'] }}` (not `~` or `lookup('env', 'HOME')`) — this is what every existing task uses and it resolves correctly under `become`.
- **APT third-party repos**: `get_url` the armoured (`.asc`) key straight into `/etc/apt/keyrings/` → register the repo with `ansible.builtin.deb822_repository`, pointing `signed_by` at that `.asc` path. `deb822_repository` accepts armoured keys, so there is no `gpg --dearmor` step. See `roles/tools/tasks/vscode.yaml` or `apt.yaml`. Don't use `apt_key` (deprecated) or inline `apt-key add`.
- **Idempotent shell-outs**: when a task can't be expressed with a module, guard it with `creates:` or a preceding `stat` + `when:` so re-runs are no-ops.
- **Upstream installer scripts**: don't hand-roll the download → run → delete sequence. `roles/tools/tasks/_install_script.yaml` implements it (including the stat guard and cleanup); include it and pass a `tools_install_script` dict — see the schema comment at the top of that file. Tools with no surrounding logic go in the `tools_install_scripts` list in `roles/tools/defaults/main.yaml`; ones that need neighbouring tasks pass the dict via `vars:` on the include (`rust.yaml`, `python.yaml`, `node.yaml`).
- **`.zshrc` edits** use `blockinfile` with a unique `marker` per block (`# {mark} ANSIBLE MANAGED BLOCK - <name>`) so each managed block can be updated/removed independently.

## Tags

Tags are the primary UX. The top-level role tag (`system`, `tools`, …) runs the whole role; each imported sub-task file adds a finer-grained tag. When adding a new sub-task file, add it to the role's `main.yaml` with both `import_tasks:` and `tags:` so it's reachable individually. The README "Available Tags" table should be kept in sync.

## Linting

`ansible-lint` runs in CI with `profile: production` and skips only `package-latest` (intentional, system upgrades) and `no-handler` (one-shot setup, no handlers). New code is expected to pass at production profile without adding to the skip list.
