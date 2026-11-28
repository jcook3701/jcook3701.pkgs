# Github CLI (gh)

[GitHub CLI](https://github.com/cli/cli) brings GitHub repositories,
pull requests, issues, and other GitHub operations to the terminal.

This Ansible Galaxy role installs GitHub CLI and manages its configuration
independently for multiple existing Linux accounts.

## Features

- Installs GitHub CLI using the operating system's package manager.
- Supports multiple existing accounts through `gh_users`.
- Defaults to the Ansible connection account.
- Resolves home directories through the system account database.
- Validates configured Linux accounts.
- Runs configuration commands as each selected Linux user.
- Preserves existing settings when optional values are empty or omitted.
- Applies changes only when a setting differs from the desired value.
- Maintains independent GitHub CLI configuration for every account.
- Supports host-specific Git protocols.
- Skips the root account.
- Does not depend on `sudo_user` or `jcook3701.utils.general`.
- Does not modify GitHub authentication tokens.

## Role Variables

| Variable | Type | Description / Choices | Default |
| :--- | :--- | :--- | :--- |
| `gh_state` | string | Lifecycle: `present`, `absent`, `teardown`. | `present` |
| `gh_debug` | boolean | Enable GitHub CLI role diagnostics. | `false` |
| `gh_users` | list of dictionaries | Existing Linux accounts for GitHub CLI configuration. Root is skipped. | Connection account |
| `gh_users[].name` | string | Existing Linux account username. | Required per entry |
| `gh_users[].gh_host` | string | GitHub hostname used for host-specific configuration. | `github.com` |
| `gh_users[].gh_account` | string | Intended GitHub identity; does not authenticate the account. | `""` |
| `gh_users[].gh_git_protocol` | string | Git protocol: `https`, `ssh`, or empty to preserve existing. | `""` |
| `gh_users[].gh_editor` | string | Editor command for GitHub CLI. Empty preserves existing. | `""` |
| `gh_users[].gh_pager` | string | Pager command for GitHub CLI. Empty preserves existing. | `""` |
| `gh_users[].gh_prompt` | string | `enabled`, `disabled`, or empty to preserve existing. | `""` |
| `gh_pkg_names` | list of strings | OS-specific packages; internal role variable. | `["gh"]` |

## Multi-User Configuration

The role accepts a list of account dictionaries using `gh_users`.

Each entry identifies an existing Linux account and provides optional
GitHub CLI preferences.

The Linux account's home directory determines where the role manages
its GitHub CLI configuration.

For example, on a typical Linux system:

- `jcook` uses `/home/jcook/.config/gh`.
- `chat-gpt` uses `/home/chat-gpt/.config/gh`.

The role uses actual home directories from the system account database
rather than assuming every account resides under `/home`.

### Centralized User Definitions

For infrastructure projects using `bootstrap_system_users`, keep each
account's GitHub CLI settings nested under the existing user definition.

For example:

```yaml
bootstrap_system_users:
  - name: "jcook"
    gh:
      enabled: true
      host: "github.com"
      account: "jcook3701"
      git_protocol: "https"
      editor: "code --wait"
      pager: "less"
      prompt: "enabled"

  - name: "chat-gpt"
    gh:
      enabled: true
      host: "github.com"
      account: ""
      git_protocol: "https"
      editor: "vi"
      pager: "cat"
      prompt: "disabled"
```

This is the input structure for the consuming configuration repository.

A separate inline template transforms these account records into the
`gh_users` variable accepted by the role.

This separation avoids duplicating user configuration across different
Ansible roles.

### Inline Template Integration

The consuming Ansible project can use:

```yaml
gh_users: >-
  {{ lookup('ansible.builtin.template',
     playbook_dir ~ '/templates/gh_users_inline.j2') | from_yaml }}
```

The inline template must generate the following fields:

- `name`
- `gh_host`
- `gh_account`
- `gh_git_protocol`
- `gh_editor`
- `gh_pager`
- `gh_prompt`

Only users with `gh.enabled: true` should appear in the generated list.

The `gh_users_inline.j2` template belongs to the consuming
`ansible-config` repository, not this reusable collection role.

If the generated list is empty, the role installs the GitHub CLI package
without modifying any user profile.

## Configuration Management

The role manages the following GitHub CLI settings:

| Field | GitHub CLI setting | Scope |
| :--- | :--- | :--- |
| `gh_git_protocol` | `git_protocol` | Configured GitHub host |
| `gh_editor` | `editor` | User configuration |
| `gh_pager` | `pager` | User configuration |
| `gh_prompt` | `prompt` | User configuration |

The role reads each existing setting using `gh config get`.

It executes `gh config set` only when the desired value differs
from the current value.

Empty values skip configuration of that setting.

The role does not overwrite other GitHub CLI preferences, extensions,
or authentication files.

## GitHub Authentication

Installing GitHub CLI and configuring its preferences does not
authenticate a GitHub account.

The `gh_account` variable records the intended GitHub identity.
It does not automatically authenticate, switch accounts, or provision
credentials.

Each Linux account must authenticate independently using an
appropriately authorized GitHub account or token.

Existing authentication remains untouched.

For automation accounts, a separately authorized and appropriately
scoped token can be used in a future authentication workflow.

Do not store personal access tokens directly in
`bootstrap_system_users` or unencrypted inventory files.

Note that `gh_prompt: "disabled"` disables interactive prompting
for that user. Authentication workflows for such accounts must
be designed accordingly.

## Lifecycle

- `present`: Installs GitHub CLI and manages selected user preferences.
- `absent`: Removes GitHub CLI packages.
- `teardown`: Removes GitHub CLI packages using the existing package
  removal workflow.

Both removal states preserve each user's GitHub CLI configuration
and authentication files.

This avoids accidentally deleting unrelated credentials or settings.
The role does not delete Linux user accounts.

## Validation

Inspect a configured user's settings:

```shell
sudo -iu jcook gh config list
```

Inspect the automation account:

```shell
sudo -iu chat-gpt gh config list
```

Check the configured Git protocol for a specific host:

```shell
sudo -iu chat-gpt gh config get git_protocol --host github.com
```

Check authentication independently:

```shell
sudo -iu chat-gpt gh auth status --hostname github.com
```

A successfully configured GitHub CLI does not necessarily mean
the account is authenticated.

## Security

The role performs system package installation with Ansible privilege
escalation.

Per-user configuration runs under each target account using
`become_user` and an account-specific home directory.

Individual accounts do not need sudo privileges.

The role does not copy authentication tokens or SSH private keys
between Linux users.

## Author Information

Maintained by **Jared W. Cook** as part of the core infrastructure and
container management ecosystem.
