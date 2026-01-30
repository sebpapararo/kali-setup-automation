# kali-setup-automation

![License](https://img.shields.io/badge/license-MIT-blue)
![Platform](https://img.shields.io/badge/platform-Kali%20Linux-557C94?logo=kalilinux&logoColor=white)
![Lint](https://github.com/sebpapararo/kali-setup-automation/actions/workflows/lint.yaml/badge.svg)

Ansible playbook for automated Kali Linux configuration. Sets up a fully configured development and security testing environment including system settings, development tools, terminal enhancements, and desktop customization.

## Quickstart

```bash
# Install Ansible via pipx
pipx install --include-deps ansible

# Run the full setup (will prompt for sudo password)
ansible-playbook site.yaml

# Or run specific components using tags (note some tags rely on others being ran first)
ansible-playbook site.yaml -t tools
ansible-playbook site.yaml -t vscode,docker,python
```

Reboot after completion for all changes to take effect.

## Available Tags

### Main Tags

| Tag | Description |
|-----|-------------|
| `desktop` | Desktop environment configuration |
| `ssh` | Generate ed25519 SSH keypair |
| `system` | System configuration (includes all system sub-tags below) |
| `terminal` | Terminal enhancements (bat, fd-find, ripgrep, fzf, shell aliases) |
| `tools` | Install all development tools (includes all tool sub-tags below) |

### System Sub-Tags

Use these to run specific system configuration tasks:

| Tag | Description |
|-----|-------------|
| `autologin` | Enable autologin for kali user |
| `cleanup` | Remove unused home directories (Music, Pictures, etc.) |
| `regional` | Regional settings (locale, keyboard, timezone) |
| `upgrade` | APT sources modernization and full package upgrade |
| `xfce` | Disable XFCE power management, screensaver, and screen lock |

### Tool Sub-Tags

Use these to install specific tools without running the full `tools` role:

| Tag | Description |
|-----|-------------|
| `apt` | APT packages (Trivy, Bruno, checksec, clangd, flameshot, gdb, ghidra, gitleaks, lldb, openjdk-21-jdk) |
| `bash` | Install tools via bash |
| `binaryninja` | Install Binary Ninja and menu shortcut |
| `chrome` | Google Chrome browser |
| `docker` | Docker CE, compose plugin, buildx plugin |
| `golang` | Go programming language |
| `node` | Node.js LTS via NVM |
| `python` | Python tools (pwntools, netexec, bandit, uv, pyenv) |
| `rust` | Rust toolchain, Starship prompt, Zellij terminal multiplexer |
| `vscode` | VS Code with extensions (BeardedTheme, Material Icons, IntelliJ keybindings, GitLens) |

### Examples

```bash
# Run only system configuration
ansible-playbook site.yaml -t system

# Install just Rust and Python tooling
ansible-playbook site.yaml -t rust,python

# Set up terminal and desktop
ansible-playbook site.yaml -t terminal,desktop
```

## Roadmap

- [ ] Chrome extensions
- [ ] Firefox extensions
- [ ] Binary Ninja installation and configuration
- [ ] Ghidra configuration
- [ ] Offline tag (offline-only tasks)
- [ ] Run against remote machine
- [ ] Ability to change username
- [ ] Ability to change password
