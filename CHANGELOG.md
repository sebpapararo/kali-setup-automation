# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.4.0] - 30-01-2026

### Added

- Added support for adding xfce4 taskbar launcher icons
- Added support for shared folders in VMware
- Added install for Binary Ninja

## [1.3.1] - 28-01-2026

### Fixed

- Fix clipboard not working from guest -> host when using zellij

## [1.3.0] - 28-01-2026

### Added

- Added gdb configuration via `~/.gdbinit`


## [1.2.0] - 28-01-2026

### Added

- Added install for pwndbg

### Fixed

- Fix the desktop wallpaper not applying properly


## [1.1.0] - 26-01-2026

### Added

- Added install for Opengrep


## [1.0.0] - 24-01-2026

### Added

- Initial Ansible playbook structure for Kali Linux automation
- System configuration role (locale, keyboard, timezone, XFCE settings, autologin)
- SSH role for ed25519 keypair generation
- Tools role with modular sub-tasks:
  - APT packages (Trivy, Bruno, checksec, clangd, flameshot, gdb, ghidra, gitleaks, lldb, openjdk-21-jdk)
  - Rust toolchain with Starship prompt and Zellij terminal multiplexer
  - Go programming language
  - Google Chrome browser
  - VS Code with extensions and custom settings
  - Docker CE with compose and buildx plugins
  - Python tools (pwntools, netexec, bandit, uv, pyenv)
  - Node.js LTS via NVM
- Terminal role (bat, fd-find, ripgrep, fzf, shell aliases)
- Desktop role for environment configuration
- Tag-based execution for selective installation
