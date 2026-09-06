# Rsyslog

[Rsyslog](https://www.rsyslog.com/) is a high-performance, open-source logging system used on Linux and Unix-like computers to collect, filter, and route event messages.

## Role Variables

| Variable | Description | Default |
| :--- | :--- | :--- |
| `rsyslog_state` | Action state for package installation or removal. Choices: `present`, `absent`. | `"present"` |
| `rsyslog_node_type` | Architecture deployment target type determining local operations or streaming topologies. Choices: `local`, `client`, `master`. | `"local"` |
| `rsyslog_users` | A declarative array of local system accounts to append to the system logging management group. Each list item is a dictionary containing:<br>• **`name`** *(str, required)*: The exact local username string to grant logging audit management access permissions. | `[{"name": "{{ ansible_user \| default(ansible_user_id) }}"}]` |
| `rsyslog_manage_group` | Controls whether the role should actively verify or generate the targeted system logging group. | `true` |
| `rsyslog_remote_server_hosts` | High-availability list of target remote log collection hostnames or IP endpoints (evaluated sequentially when `rsyslog_node_type` is 'client'). | `["syslog.example.com"]` |
| `rsyslog_remote_server_port` | Target destination transport port for remote event streaming paths. | `514` |
| `rsyslog_remote_protocol` | Underlying network transport socket protocol utilized for remote shipping layers. Choices: `udp`, `tcp`. | `"udp"` |
| `rsyslog_file_create_mode` | Default filesystem permissions applied to newly created log output files. | `"0640"` |
| `rsyslog_dir_create_mode` | Default filesystem permissions applied to newly generated parent log directory hierarchies. | `"0755"` |
| `rsyslog_umask` | Process file mode creation umask boundary assigned to the running rsyslog daemon process environment. | `"0022"` |
| `rsyslog_facility_rules` | Pluggable facilities matching rules matrix mapping daemon logging channels straight into target files or endpoints. Each list item is a dictionary containing:<br>• **`rule`** *(str, required)*: Standard rsyslog facility-priority selector filter string.<br>• **`target`** *(str, required)*: Output file directory storage location or remote streaming reference string. | *(See `defaults/main.yml` for default selectors matrix)* |

## Configuration Examples

### Example 1: Standalone Local Logging Node

Perfect for secure, independent servers tracking infrastructure events strictly on local storage disk arrays.

```yaml
rsyslog_state: "present"
rsyslog_node_type: "local"
```

### Example 2: Resilient Network Client Log Transmitter

Perfect for corporate application nodes securely streaming event pipelines outbound to a central aggregation pool.

```yaml
rsyslog_state: "present"
rsyslog_node_type: "client"
rsyslog_remote_server_hosts: ["syslog.example.com"]
rsyslog_remote_server_port: 514
rsyslog_remote_protocol: "tcp"
```

### Example 3: Centralized Infrastructure Log Aggregator Master

Perfect for master repository servers opening socket interfaces to ingest and consolidate remote cross-node log volumes.

```yaml
rsyslog_state: "present"
rsyslog_node_type: "master"
rsyslog_remote_server_port: 514
```

## Author Information

Maintained by **Jared Cook** as part of the core infrastructure and container management ecosystem.

<!--
## Authors Notes

-->
