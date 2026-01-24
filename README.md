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

# Or run specific components using tags
ansible-playbook site.yaml -t tools
ansible-playbook site.yaml -t vscode,docker,python
```

Reboot after completion for all changes to take effect.

## Available Tags

### Main Tags

| Tag | Description |
|-----|-------------|
| `system` | System configuration (includes all system sub-tags below) |
| `ssh` | Generate ed25519 SSH keypair |
| `tools` | Install all development tools (includes all tool sub-tags below) |
| `terminal` | Terminal enhancements (bat, fd-find, ripgrep, fzf, shell aliases) |
| `desktop` | Desktop environment configuration |

### System Sub-Tags

Use these to run specific system configuration tasks:

| Tag | Description |
|-----|-------------|
| `upgrade` | APT sources modernization and full package upgrade |
| `locale` | Set locale to en_GB.UTF-8 |
| `keyboard` | Configure keyboard layout (UK) |
| `timezone` | Set timezone (Europe/London) |
| `autologin` | Enable autologin for kali user |
| `xfce` | Disable XFCE power management, screensaver, and screen lock |
| `cleanup` | Remove unused home directories (Music, Pictures, etc.) |

### Tool Sub-Tags

Use these to install specific tools without running the full `tools` role:

| Tag | Description |
|-----|-------------|
| `apt` | APT packages (Trivy, Bruno, checksec, clangd, flameshot, gdb, ghidra, gitleaks, lldb, openjdk-21-jdk) |
| `rust` | Rust toolchain, Starship prompt, Zellij terminal multiplexer |
| `golang` | Go programming language |
| `chrome` | Google Chrome browser |
| `vscode` | VS Code with extensions (BeardedTheme, Material Icons, IntelliJ keybindings, GitLens) |
| `docker` | Docker CE, compose plugin, buildx plugin |
| `python` | Python tools (pwntools, netexec, bandit, uv, pyenv) |
| `node` | Node.js LTS via NVM |

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
- [ ] Taskbar icons
- [ ] Configurable keyboard layout and language
- [ ] Offline tag (offline-only tasks)
- [ ] Run against remote machine
- [ ] Ability to change username
