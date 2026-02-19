# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.6.0] - 19-02-2026

### Added

- Added `strace` to apt packages
- Added install for nuclei via `go install`
- Added cloning of PayloadsAllTheThings to `~/Documents`
- Added `~/go/bin` to PATH in zshrc alongside Go itself

### Changed

- Removed Ghidra from taskbar launchers
- Removed Ghidra configuration from README TODO list
- Scoped `become: true` to only the unarchive task in the Go install block, rather than the whole block
- Remove conflicting pwntools `checksec` binary after installing the GitHub version

## [1.5.1] - 14-02-2026

### Changed

- Install `checksec` from GitHub instead of default apt reposiotry to ensure latest version

### Fixed

- Fix autologin and binaryninja taskbar icon for non-default usernames
- Fix rockyou.txt permissions

## [1.5.0] - 12-02-2026

### Added

- Added apt packages: jq, name-that-hash, seclists
- Added rockyou.txt extraction from seclists
- Added install for Penelope via pipx
- Added install for tokei via cargo
- Added sensible git configurations

### Changed

- Shortened Binary Ninja desktop entry comment
- Consolidated netexec install into the shared pipx loop
- Updated README to reflect Binary Ninja installation is done (configuration remains)

## [1.4.1] - 30-01-2026

### Changed

- Restructure the locale, timezone, and keyboard functionality into a single `regional` task file
- Housekeeping on README.md

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
