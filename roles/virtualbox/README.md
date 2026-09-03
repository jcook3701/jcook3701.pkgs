# Virtualbox

[VirtualBox](https://www.virtualbox.org/) is a free, open-source hosted hypervisor developed by Oracle that allows you to run multiple operating systems (OS) simultaneously on a single physical machine.  

## Features

* **Cross-Platform Topology Routing:** Works natively with a decoupled utility architecture (`repo_add`) to establish upstream repository tracking for APT and DNF systems while leveraging native DKMS structures on Arch Linux.
* **Granular Version Selector Matrix:** Features a unified software mapping matrix supporting major hypervisor life-cycles (`6.1`, `7.0`, `7.1`, and upcoming `7.2` editions).
* **Automatic Kernel Module Management:** Built-in safeguards to monitor and verify necessary system compilation groups, driving driver rebuild routines automatically via host kernel structures.
* **Strict Network Isolation Enforcement:** Renders global security whitelists (`/etc/vbox/networks.conf`) to control, audit, and restrict local unprivileged host bridge CIDR blocks.
* **Persistent Application Tuning:** Coordinates target storage adjustments through non-destructive application property hooks rather than fragile inline XML templates.

---

## Role Variables

| Variable | Description | Default |
| :--- | :--- | :--- |
| **`virtualbox_state`** | Targeted structural installation state (`present` or `absent`). | `"present"` |
| **`virtualbox_users`** | A declarative array of local system accounts appended to the hypervisor execution group. | `[]` |
| **`virtualbox_manage_group`** | Toggles whether the role ensures the foundational hypervisor execution group is actively maintained. | `true` |
| **`virtualbox_install_extension_pack`** | Controls whether the Oracle VM Extension Pack (enabling VRDE, USB 3.0, and NVMe boot) is deployed. | `true` |
| **`virtualbox_selected`** | The major package matrix version selector utilized to map platform package names. | `"virtualbox_7_1"` |
| **`virtualbox_download_url`** | The primary upstream URL base path used to fetch individual Extension Pack files. | `"https://virtualbox.org"` |
| **`virtualbox_enable_dkms`** | Enforces continuous module tracking to compile drivers automatically upon host kernel upgrades. | `true` |
| **`virtualbox_recompile_drivers`** | Toggles whether tasks should run a fallback recompilation swipe if kernel drivers are missing. | `true` |
| **`virtualbox_manage_net_policy`** | Determines whether the role strictly renders the global host-only networking access whitelist sheet. | `true` |
| **`virtualbox_hostonly_allowed_subnets`** | CIDR blocks that unprivileged local users are authorized to bind when allocating bridge interfaces. | `["192.168.56.0/21"]` |
| **`virtualbox_default_machine_folder`** | An absolute path to relocate default VM disk creation space away from the user's home partition. | `""` |
| **`virtualbox_headless_enabled`** | Toggles whether VM execution tasks omit graphic user interfaces, optimizing execution for servers. | `false` |
| **`virtualbox_headless_vrde_port`** | The default TCP listener port assigned to surface the structural VRDP connection matrix. | `3389` |
| **`virtualbox_global_properties_custom`** | A free-form nested map passed downwards to apply unstructured global preferences via `VBoxManage`. | `{}` |

---

## Example Playbooks

### 1. Standard Enterprise Workstation Deployment

Deploys VirtualBox 7.1 alongside compilation headers and the official Extension Pack, granting local administrators hypervisor privileges.

```yaml
- name: Deploy Standard Hypervisor Node
  hosts: workstations
  become: true
  roles:
    - role: jcook3701.pkgs.virtualbox
      vars:
        virtualbox_users:
          - name: "jcook"
          - name: "sysadmin"
```

### 2. Headless Server Node with Isolated Disk Allocation

Configures VirtualBox 7.0 on an unheaded headless compute cluster, rerouting guest disk generation paths to a fast dedicated storage volume.

```yaml
- name: Deploy Headless Virtualization Pool
  hosts: compute_servers
  become: true
  roles:
    - role: jcook3701.pkgs.virtualbox
      vars:
        virtualbox_selected: "virtualbox_7_0"
        virtualbox_headless_enabled: true
        virtualbox_default_machine_folder: "/mnt/nvme-pool/virtualbox-vms"
        virtualbox_hostonly_allowed_subnets:
          - "10.10.56.0/24"
          - "192.168.100.0/22"
```

### 3. Hypervisor Tear Down / Decommissioning

Safely disables execution privileges, uninstalls core binary packages, stops runtime drivers, and purges structural network tracking sheets.

```yaml
- name: Decommission Virtualization Nodes
  hosts: legacy_hosts
  become: true
  roles:
    - role: jcook3701.pkgs.virtualbox
      vars:
        virtualbox_state: "absent"
```

---

## Author Information

Maintained by **Jared Cook** as a core component of the private virtualization infrastructure catalog.

<!--

## Authors Notes
Setup **VirtualBox** repository and install version 7.1.

**virtualbox_selected** Options:

* virtualbox_6_1
* virtualbox_7_0
* virtualbox_7_1
* virtualbox_7_2

``` shell
$ ansible-playbook jcook3701.pkgs.virtualbox.yml -K -e "virtualbox_selected=virtualbox_7_1"
```
-->
