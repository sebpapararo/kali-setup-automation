# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [1.11.0] - 07-07-2026

### Added

- Added apt packages: gdbserver, goshs
- Added Trufflehog install (via upstream installer script) to the `bash` task
- Added dive install (via `.deb`) to the `git` task
- Added pipx packages: bloodyAD, git-dumper
- Added `rusthound-ce` to cargo installs
- Added tool repos cloned to `~/Documents/tools/`: PRET, adPEAS

### Changed

- Replaced `penelope` (installed from `git+https://github.com/brightio/penelope`) with the `penelope-shell-handler` pipx package

### Removed

- Removed `menulibre` from the desktop role apt packages

## [1.10.0] - 13-05-2026

### Added

- Added new `obsidian` task to install Obsidian and extract a base vault into `~/Documents/Obsidian Job Notes/`
- Added new `custom` task to deploy in-house scripts to `~/Documents/tools/custom/` (currently ships `nmap_to_md.py`)
- Added apt package: sippts
- Added pipx package: defaultcreds-cheat-sheet

## [1.9.1] - 08-05-2026

### Added

- Added small SSH config to assist in connecting to older hosts

### Fixed

- Fix nvm installer location by setting `NVM_DIR` to `~/.config/nvm`

## [1.9.0] - 30-04-2026

### Added

- Added apt packages: jadx, snmp-mibs-downloader
- Added `angr` to global pip packages
- Added pipx packages: clairvoyance, smbclientng

### Removed

- Removed pyenv install

## [1.8.0] - 07-04-2026

### Added

- Added apt packages: awscli, feroxbuster, sstimap, wpprobe, xsstrike
- Added cheatsheet repo cloned to `~/Documents/cheatsheets/`: WADComs
- Added retries (3 attempts, 3s delay) to git clone and file download tasks for improved reliability
- Set QTerminal transparency to 0 via qterminal.ini

## [1.7.0] - 13-03-2026

### Added

- Added apt packages: bettercap, bloodhound, cmake, cupp, cyberchef, enum4linux-ng, gowitness, ipcalc, ipmitool, kubectl, libreadline-dev, ltrace, lynis, mdns-scan, mongodb-clients, nbtscan-unixwiz, ntpsec, nuclei, odat, starship, tokei, xrdp
- Added `nmap` alias (`sudo nmap`) to shell aliases
- Added new cheatsheet repos cloned to `~/Documents/cheatsheets/`: InternalAllTheThings, HackTricks, reverse-shell-generator, GTFObins, LOLBAS, personal-pentesting-notes, endoflife.date
- Added new tool repos cloned to `~/Documents/tools/`: testssl.sh, PowerSharpPack
- Added exploit repo cloned to `~/Documents/exploits/`: mongobleed
- Added downloads to `~/Documents/tools/`: PrivescCheck.ps1, pspy (32/64-bit variants), linux-exploit-suggester (les.sh), ligolo-ng (agent + proxy, Linux and Windows), RustScan
- Added new `gem` task to install `evil-winrm` and `readline-ext` via gem
- Added new `nessus` task to download and install Nessus
- Added new `windows` task to download and extract Sysinternals Suite
- Added pipx packages: updog, ssh-audit, wesng (with chardet injected as a dependency)
- Added `~/Documents/cheatsheets/`, `~/Documents/exploits/`, `~/Documents/tools/`, and `~/Documents/tools/pspy/` directories
- Added Firefox as the default handler for http/https/html MIME types
- Added `rustscan` and `legba` to cargo installs
- Perform first-run of Nuclei after install to download templates
- Run `apt autoremove --purge` after package installation
- Remove compressed copies of rockyou.txt after extraction

### Changed

- Moved starship from cargo to apt
- Moved tokei from cargo to apt
- Starship zshrc configuration block moved from `rust.yaml` to `apt.yaml`
- Replaced single PayloadsAllTheThings clone with a loop-based approach covering multiple repos
- checksec download URL updated to use the `/latest/` redirect
- evil-winrm removed from apt and replaced with gem install
- rockyou.txt extraction now checks whether the archive exists before attempting to extract

### Fixed

- Desktop taskbar paths now use `ansible_facts['env']['HOME']` instead of `~` to support non-default usernames

## [1.6.0] - 19-02-2026

### Added

- Added `strace` to apt packages
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
