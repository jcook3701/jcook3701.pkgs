# Git

[Git](https://git-scm.com/) is a free and open source distributed version
control system designed to handle everything from small to very large
projects with speed and efficiency.

This Ansible Galaxy role installs Git and manages Git identities
independently for multiple existing Linux accounts.

## Features

- Installs Git using the target operating system's package manager.
- Supports multiple users through the `git_users` list.
- Defaults to the Ansible connection account.
- Resolves user home directories through the system account database.
- Validates that configured Linux accounts already exist.
- Configures Git commit names and email addresses independently per user.
- Preserves existing Git settings when their corresponding values are omitted.
- Skips the root account.
- Does not use `sudo_user` or require `jcook3701.utils.general`.
- Supports the existing `present`, `absent`, and `teardown` lifecycle states.

## Role Variables

| Variable | Type | Description / Choices | Default |
| :--- | :--- | :--- | :--- |
| `git_state` | string | Lifecycle state: `present`, `absent`, `teardown`. | `present` |
| `git_debug` | boolean | Enable Git role diagnostics. | `false` |
| `git_users` | list of dictionaries | Existing Linux accounts for per-user Git configuration. Root is skipped. | `[{"name": "{{ ansible_user \| default(ansible_user_id) }}"}]` |
| `git_users[].name` | string | Required existing Linux account username. | Required per entry |
| `git_users[].git_name` | string | Optional Git commit author name (`user.name`). | Unchanged if omitted |
| `git_users[].git_email` | string | Optional Git commit author email (`user.email`). | Unchanged if omitted |
| `git_pkg_names` | list of strings | OS-specific Git packages. Internal role variable. | `["git"]` |

## Example Playbook

The consuming playbook or inventory provides the list of accounts
to manage.

```yaml
---
- name: Install Git and configure developer accounts
  hosts: workstations
  become: true
  roles:
    - role: "jcook3701.pkgs.git"
      vars:
        git_state: present
        git_users:
          - name: "developer"
            git_name: "Developer Name"
            git_email: "developer@example.com"
          - name: "automation"
            git_name: "Automation"
            git_email: "automation@example.com"
```

The example usernames and email addresses are placeholders.

Each user must already exist on the managed system.

No user account creation occurs in this role.

## Multi-User Configuration

The `name` field identifies the local Linux account.

The `git_name` and `git_email` fields configure that account's
Git commit identity.

For example:

```yaml
git_users:
  - name: "developer"
    git_name: "Developer Name"
    git_email: "developer@example.com"

  - name: "automation"
    git_name: "Automation"
    git_email: "automation@example.com"
```

The role configures each account independently using its own home
directory and permissions.

Git stores the account-level identity in the user's global Git
configuration.

The role does not configure system-wide Git identity settings.

An empty list disables per-account configuration:

```yaml
git_users: []
```

Git packages are still installed when `git_state` is `present`.

If `git_name` is omitted, an existing `user.name` value is preserved.

If `git_email` is omitted, an existing `user.email` value is preserved.

## Lifecycle

- `present`: Installs Git and manages explicitly configured Git identity
  values for selected accounts.
- `absent`: Removes the Git packages according to the existing role behavior.
- `teardown`: Performs the existing package removal workflow.

Neither `absent` nor `teardown` deletes users' home directories or
removes their existing `.gitconfig` files.

This preserves the current role's lifecycle behavior and avoids
deleting unrelated personal Git configuration.

## Security and Permissions

Ansible uses privilege escalation for system package management and
to switch to each configured local account.

Individual accounts do not require sudo privileges.

The role does not manage Git credentials, SSH private keys, GitHub
authentication tokens, or credential helpers.

These responsibilities remain separate from Git commit identity.

## Validation

After deployment, inspect a configured user's identity:

```shell
sudo -iu developer git config --global --get user.name
sudo -iu developer git config --global --get user.email
```

Replace `developer` with the target Linux account.

## Author Information

Maintained by **Jared W. Cook** as part of the core infrastructure and
container management ecosystem.
