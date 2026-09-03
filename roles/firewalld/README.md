# Firewalld

[Firewalld](https://firewalld.org/) provides a dynamically managed firewall with support for network/firewall zones that define the trust level of network connections or interfaces. It has support for IPv4, IPv6 firewall settings, ethernet bridges and IP sets. There is a separation of runtime and permanent configuration options. It also provides an interface for services or applications to add firewall rules directly.

## Role Variables

| Variable | Description | Default |
| :--- | :--- | :--- |
| `firewalld_state` | Lifecycle execution state for package installation or removal. Choices: `present`, `absent`. | `"present"` |
| `firewalld_default_zone` | Default operational zone assignment for new system network interfaces. | `"public"` |
| `firewalld_permanent` | Define whether rules should be persistently written to disk (permanent) or applied only to the active runtime context. | `true` |
| `firewalld_zones` | A matrix dictionary defining firewalld zones. Key is the zone name (e.g., `public`, `internal`). Values inside each zone can declare:<br>• **`services`** *(list of str)*: Allowed named system services.<br>• **`ports`** *(list of str)*: Target custom port and protocol strings.<br>• **`masquerade`** *(bool)*: Whether network address masquerading is enabled.<br>• **`sources`** *(list of str)*: Specific client source CIDR networks or IP address ranges assigned to the zone.<br>• **`interfaces`** *(list of str)*: Physical system network cards explicitly bound to the zone. | *(See `defaults/main.yml` for template object)* |
| `firewalld_custom_services` | Add user-defined custom service structures to `/etc/firewalld/services/`. Each list item is a dictionary containing:<br>• **`name`** *(str, required)*: File-safe name reference for the service entry.<br>• **`short`** *(str, optional)*: Short user-friendly label description.<br>• **`description`** *(str, optional)*: Deep conceptual breakdown outlining why this service exception exists.<br>• **`ports`** *(list of str, required)*: Specific internal application entry configurations like `['9000/tcp', '9001/udp']`. | `[]` |

## Author Information

Maintained by **Jared Cook** as part of the core infrastructure and container management ecosystem.

<!--
# Example:

- name: Request firewall access for Webmin interface
  ansible.builtin.include_role:
    name: firewalld
    tasks_from: create_service
  vars:
    firewalld_in_name: "webmin"
    firewalld_in_short: "Webmin"
    firewalld_in_description: "Webmin web-based system administration interface"
    firewalld_in_ports:
      - "10000/tcp"
  when: webmin_enabled | bool

-->
