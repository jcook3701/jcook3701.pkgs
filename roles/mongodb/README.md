# MongoDB

[MongoDB](https://www.mongodb.com/company/what-is-mongodb) is a distributed NoSQL document database that stores data in flexible, JSON-like structures instead of traditional rows and columns.

## Role Variables

| Variable | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| **`mongodb_state`** | `string` | `"present"` | Structural lifecycle target execution state (`present`, `absent`, or `teardown`). |
| **`mongodb_download_url`** | `string` | `"https://mongodb.org"` | Upstream network base mirror server hosting primary installation packages. |
| **`mongodb_version`** | `string` | `"8.0"` | The primary target version string used for building repository strings dynamically. |
| **`mongodb_security_authorization`** | `string` | `"enabled"` | Enforces Role-Based Access Control (RBAC) to ensure client systems must authenticate. |
| **`mongodb_tls_mode`** | `string` | `"disabled"` | Network transport layer crypto setting (`disabled`, `allowTLS`, `preferTLS`, `requireTLS`). |
| **`mongodb_tls_certificate_key_file`** | `string` | `""` | Filepath pointing to the server's combined TLS public certificate and private key. |
| **`mongodb_tls_ca_file`** | `string` | `""` | Filepath pointing to the root Certificate Authority used to validate incoming nodes. |
| **`mongodb_security_keyfile_contents`** | `string` | `""` | The shared string block used to populate the cluster signature file for replica validation. |
| **`mongodb_security_keyfile_path`** | `string` | `"/var/lib/mongodb/pki/cluster.key"` | Absolute target disk destination path where the cluster signature key is dropped. |
| **`mongodb_net_port`** | `integer` | `27017` | The bound TCP network execution loop listening port. |
| **`mongodb_net_bind_ip`** | `string` | `"127.0.0.1"` | Comma-separated list of interface IP addresses listening for active socket bindings. |
| **`mongodb_net_max_incoming_connections`** | `integer` | `65536` | Upper limitation cap checking maximum simultaneous open client communication blocks. |
| **`mongodb_storage_engine`** | `string` | `"wiredTiger"` | Core disk engine layout pattern selection (`wiredTiger`, `ephemeralForTest`, `inMemory`). |
| **`mongodb_wiredtiger_cache_size_gb`** | `string` | `""` | Explicit maximum RAM execution threshold ceiling allocated to the engine cache. |
| **`mongodb_storage_journal_enabled`** | `boolean` | `true` | Toggles write-ahead logging operation durability parameters to prevent system crashes. |
| **`mongodb_storage_directory_per_db`** | `boolean` | `true` | Separates discrete structural database layers into isolated OS folders on disk. |
| **`mongodb_replset_name`** | `string` | `""` | Declares the cluster identity name used to pull discrete standalone instances into a shared sync array. |
| **`mongodb_ulimit_nofile`** | `integer` | `64000` | Sets the ceiling threshold for the maximum count of concurrent open file descriptors. |
| **`mongodb_ulimit_nproc`** | `integer` | `64000` | Limits scheduling thread execution ceiling sizes for processing query loops. |
| **`mongodb_ulimit_memlock`** | `string` | `"unlimited"` | Prevents operating system file-system paging layers from swapping out memory blocks. |

## Author Information

Maintained by **Jared Cook** as part of the core infrastructure and container management ecosystem.

<!--
## Authors Notes

-->
