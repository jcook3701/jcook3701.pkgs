# [NVM](https://github.com/nvm-sh/nvm)

Ansible Galaxy role for installing and removing Node Version Manager (NVM) for
multiple **existing** local users. NVM itself manages Node.js versions per
user and per shell. This role installs NVM, not Node.js versions.

## Features

- Uses a declarative list of user dictionaries, matching `sdkman_users` and
  `docker_ce_users` patterns.
- Defaults to the Ansible connection account; no personal usernames or paths.
- Determines user home directories from the system account database.
- Skips root and leaves already-installed NVM instances unchanged.
- Installs required `git` and `curl` packages.
- Supports `present`, `absent`, and `teardown` lifecycle states.
- Does not call `jcook3701.utils.general` or depend on `sudo_user`.

## Role Variables

| Variable | Type | Description / Choices | Default |
| :--- | :--- | :--- | :--- |
| `nvm_state` | string | `present` installs, `absent` removes NVM, `teardown` also removes managed shell initialization. | `present` |
| `nvm_debug` | boolean | Display NVM role configuration when enabled. | `false` |
| `nvm_users` | list of dictionaries | Existing local accounts, each with required `name`. Root is skipped. | `[{"name": "{{ ansible_user \| default(ansible_user_id) }}"}]` |
| `nvm_repo_url` | string | Pinned URL for the NVM installer. | `https://raw.githubusercontent.com/nvm-sh/nvm/v0.41.0/install.sh` |
| `nvm_pkgs` | list of strings | Prerequisite packages. | `["git", "curl"]` |
| `nvm_file.script` | string | Base path for an unpredictable temporary installer file. | `/tmp/nvm-install.sh` |

`nvm_file.script` is defined in `vars/main.yml` as an internal staging setting.
`nvm_repo_url` is defined only in `defaults/main.yml` so an inventory override
works as expected.

## Example Playbook

Declare the user list in the consuming playbook or inventory:

```yaml
---
- name: Install NVM for developer accounts
  hosts: workstations
  become: true
  roles:
    - role: "jcook3701.pkgs.nvm"
      vars:
        nvm_users:
          - name: "developer"
          - name: "automation"
```

To skip user installation, set `nvm_users: []`. Accounts must exist already.

## Lifecycle

- `present`: installs NVM for missing accounts. Does not upgrade existing NVM
  installations or install any Node.js release.
- `absent`: removes each selected user's `~/.nvm` directory. This also removes
  Node.js versions installed inside NVM.
- `teardown`: performs `absent` and removes NVM initialization lines from
  `.bashrc`, `.bash_profile`, `.bash_login`, `.profile`, `.zshrc`, and `.zprofile`.

NVM installation changes the selected user's shell startup file. A new shell
session is needed before `nvm` is available as a shell function. To install
Node.js 24 after NVM is available, run the following **as that user**:

```bash
nvm install 24
nvm alias default 24
nvm use 24
node --version
npm --version
npx --version
```

The role stages a root-owned executable installer in a unique temporary file,
then runs it with each selected user's privileges and `HOME`/`NVM_DIR`.
A successful run removes the temporary installer. Without an Ansible
`always` block, a failed installation may leave the temporary file behind.

## Author Information

Maintained by **Jared Cook** as part of the core infrastructure and container management ecosystem.
