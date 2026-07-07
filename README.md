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

## Running Against a Remote Host

Ensure the target host has SSH running and is accessible from this machine.

Add your target host to `inventory/hosts.yaml` under the `remote` group:

```yaml
remote:
  hosts:
    kali-target:
      ansible_host: 192.168.1.100
      ansible_user: kali
```

Then run the playbook targeting that group or host. You will be prompted for the SSH password and sudo password:

```bash
# Run against all remote hosts
ansible-playbook site.yaml --limit remote

# Run against a specific host
ansible-playbook site.yaml --limit kali-target

# Run specific tags against a remote host
ansible-playbook site.yaml --limit kali-target -t tools
```

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
| `autologin` | Enable autologin for current user |
| `cleanup` | Remove unused home directories (Music, Pictures, etc.) |
| `regional` | Regional settings (locale, keyboard, timezone) |
| `shared_folder` | Enable VMware shared folders via `/etc/fstab` (vmhgfs-fuse) |
| `upgrade` | APT sources modernization and full package upgrade |
| `xfce` | Disable XFCE power management, screensaver, and screen lock |

### Tool Sub-Tags

Use these to install specific tools without running the full `tools` role:

| Tag | Description |
|-----|-------------|
| `apt` | APT packages (Trivy, Bruno, checksec, clangd, flameshot, gdb, ghidra, gitleaks, goshs, lldb, openjdk-21-jdk, and many more) |
| `bash` | Tools installed via upstream bash installers (Opengrep, pwndbg for GDB & LLDB, Trufflehog) |
| `binaryninja` | Install Binary Ninja and menu shortcut |
| `chrome` | Google Chrome browser |
| `custom` | Deploy in-house scripts to `~/Documents/tools/custom/` |
| `docker` | Docker CE, compose plugin, buildx plugin |
| `gem` | Ruby gems (evil-winrm, readline-ext) |
| `git` | Global Git defaults, checksec/dive `.deb` installs, and clone pentest cheatsheet/tool/exploit repos plus standalone downloads (pspy, PrivescCheck, les.sh, ligolo-ng, RustScan) into `~/Documents/` |
| `golang` | Go programming language |
| `nessus` | Download and install Tenable Nessus |
| `node` | Node.js LTS via NVM |
| `obsidian` | Install Obsidian and extract base vault to `~/Documents/Obsidian Job Notes/` |
| `python` | Python tools (pwntools, angr, netexec, bandit, uv) |
| `rust` | Rust toolchain, Starship prompt, Zellij terminal multiplexer |
| `vscode` | VS Code with extensions (BeardedTheme, Material Icons, IntelliJ keybindings, GitLens) |
| `windows` | Download and extract Sysinternals Suite to `~/Documents/tools/Sysinternals/` |

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
- [ ] Binary Ninja configuration
- [ ] Offline tag (offline-only tasks)
- [ ] Ability to change username
- [ ] Ability to change password
