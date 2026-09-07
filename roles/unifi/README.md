# Unifi

## Role Variables

| Variable | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| **`unifi_os_state`** | `string` | `"present"` | Structural lifecycle target execution state (`present`, `absent`, or `teardown`). |
| **`unifi_users`** | `list` | `[{"name": "{{ ansible_user \| default(ansible_user_id) }}"}]` | Accounts granted rootless or direct access to the unifi daemon socket. Each list item is a dictionary containing:<br>• **`name`** *(str, required)*: The exact local username string to grant UniFi daemon socket access. |
| **`unifi_manage_group`** | `bool` | `true` | Controls whether the role should actively manage the lifecycle of the 'unifi' system group. |
| **`unifi_download_url`** | `string` | `"https://www.ui.com"` | The upstream base mirror server URL hosting UniFi application source distribution packages. |
| **`unifi_version`** | `string` | `"10.4"` | The major version suite target for the UniFi APT repository (e.g., `"10.4"`, `"8.6"`). |
| **`unifi_jvm_init_heap_size`** | `string` | `"1024m"` | Initial memory floor assigned directly to the running Java Virtual Machine environment. |
| **`unifi_jvm_max_heap_size`** | `string` | `"2024m"` | Maximum ceiling constraint for memory allocation before Java throws out-of-memory faults. |
| **`unifi_jvm_extra_opts`** | `string` | `"-XX:+UseG1GC..."` | Appended performance optimization flags passed straight to the Java execution engine daemon. |
| **`unifi_db_mongo_connections_max`** | `integer` | `100` | Upper connection handle socket cap used when establishing application query processing loops. |
| **`unifi_db_mongo_timeout_ms`** | `integer` | `5000` | Maximum transaction duration threshold before a dead database request throws error faults. |
| **`unifi_port_inform`** | `integer` | `8080` | TCP port handling incoming device communication and adoption heartbeats. |
| **`unifi_port_https`** | `integer` | `8443` | The primary web UI browser interface management portal listening port. |
| **`unifi_port_api_redirect`** | `integer` | `8843` | Secure routing bridge callback intercept redirect endpoint tracking port. |
| **`unifi_port_portal_http`** | `integer` | `8880` | Standard web page capture channel for local open captive visitor captive portals. |
| **`unifi_port_portal_https`** | `integer` | `8843` | Encrypted landing engine endpoint used for parsing verified secure visitor access tokens. |
| **`unifi_port_discovery_udp`** | `integer` | `10001` | UDP broadcast network scanning listener for automated local device discovery. |
| **`unifi_port_stun_udp`** | `integer` | `3478` | Session Traversal Utilities for NAT (STUN) network synchronization processing port. |
| **`unifi_port_speedtest`** | `integer` | `6789` | Internal speed testing performance throughput metric capture loop socket. |
| **`unifi_system_backup_enabled`** | `boolean` | `true` | Toggles background site recovery auto-backup creation routines on or off. |
| **`unifi_system_backup_retention_max`** | `integer` | `30` | Sets the file execution retention limit threshold count before old archives are auto-purged. |
| **`unifi_system_bind_ip`** | `string` | `""` | Binds UniFi web interfaces to a specific IP address. Blank binds to all adapters. |
| **`unifi_system_analytics_enabled`** | `boolean` | `false` | Disables telemetry tracking diagnostics from sending data upstream to Ubiquiti. |

## Author Information

Maintained by **Jared Cook** as part of the core infrastructure and container management ecosystem.

<!--
## Authors Notes

-->
