# sdkman

Meet [SDKMAN!](https://sdkman.io/) – your reliable companion for effortlessly managing multiple Software Development Kits on Unix systems. Imagine having different versions of SDKs and needing a stress-free way to switch between them. SDKMAN! steps in with its easy-to-use Command Line Interface (CLI) and API. Formerly known as GVM, the Groovy enVironment Manager, SDKMAN! draws inspiration from familiar tools like apt, pip, RVM, and rbenv and even Git. Think of it as your helpful toolkit friend, ready to streamline SDK management for you. 🛠️

## Features

- Uses a declarative list of user dictionaries, matching the `docker_ce_users` convention.
- Defaults to the Ansible connection account; no personal usernames are embedded in the role.
- Resolves each account's home directory from the system password database.
- Installs the prerequisite `zip`, `unzip`, and `curl` packages.
- Skips already-installed SDKMAN instances and does not install for `root`.
- Does not depend on `jcook3701.utils.general` or `sudo_user`.

## Role Variables

| Variable | Type | Description / Choices | Default |
| :--- | :--- | :--- | :--- |
| `sdkman_state` | string | `present` installs SDKMAN; other values skip installation. | `present` |
| `sdkman_users` | list of dictionaries | Existing local user accounts with a required `name` key. Root is skipped. | `[{"name": "{{ ansible_user \| default(ansible_user_id) }}"}]` |
| `sdkman_base_url` | string | SDKMAN installer download URL. | `https://get.sdkman.io` |

## Example Playbook

The consuming playbook or inventory controls the target users:

```yaml
---
- name: Install SDKMAN for developer accounts
  hosts: workstations
  become: true
  roles:
    - role: "jcook3701.pkgs.sdkman"
      vars:
        sdkman_users:
          - name: "developer"
          - name: "builduser"
```

Use `sdkman_users: []` to disable per-user installations. The accounts must
already exist. This role does not create local users or install SDK candidates.

## Author Information

Maintained by **Jared Cook** as part of the core infrastructure and container management ecosystem.
