# Cockpit

[Cockpit](https://cockpit-project.org/) is an interactive server admin interface. It is easy to use and very lightweight. Cockpit interacts directly with the operating system from a real Linux session in a browser.

## Role Variables

| Variable | Default Value | Type | Choices | Description |
| :--- | :--- | :--- | :--- | :--- |
| `cockpit_state` | `present` | String | `present`, `absent`, `teardown` | Controls the lifecycle state of Cockpit services and packages. |
| `cockpit_node_type` | Controls the operational profile of the Cockpit deployment layout. <br>Choices: `master`, `client` | `"client"` |

## Configuration Examples

### Example: Central Monitoring Node (Master Console)

Provisions a host to serve as the main web interface access point for managing an entire data center tier.

```yaml
# host_vars/monitor-hub.yml context
---
cockpit_state: present
cockpit_node_type: "master"
```

## Author Information

Maintained by **Jared Cook** as part of the core infrastructure and container management ecosystem.
