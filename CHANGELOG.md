# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

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
