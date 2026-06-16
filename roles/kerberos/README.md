# Kerberos

[Kerberos](https://web.mit.edu/kerberos/) is a powerful network authentication protocol developed by MIT that uses secret-key cryptography to securely verify a user's or host's identity across an insecure network. It completely eliminates the need to send passwords over the wire, making it a foundational component of Single Sign-On (SSO) systems.


``` shell
  ┌────────────────────────────────────────────────────────┐
  │                   MASTER KDC SERVER                    │
  │                                                        │
  │   ┌───────────────────┐        ┌───────────────────┐   │
  │   │     krb5-kdc      │        │    krb5-init /    │   │
  │   │ (Authentication)  │        │   cron database   │   │
  │   └─────────▲─────────┘        └─────────┬─────────┘   │
  │             │                            │             │
  │             │ Reads                      │ Runs kprop  │
  │             │                            ▼             │
  │      ┌──────┴────────────────────────────┴──────┐      │
  │      │       Master Kerberos Database           │      │
  │      │       (/var/lib/krb5kdc/principal)       │      │
  │      └──────▲───────────────────────────────────┘      │
  │             │                                          │
  │             │ Modifies                                 │
  │   ┌─────────┴─────────┐                                │
  │   │    krb5-admin     │                                │
  │   │    (kadmind)      │                                │
  │   └─────────▲─────────┘                                │
  └─────────────┼────────────────────────────┼─────────────┘
                │                            │
  Admin Request │ (kadmin)                   │ Database Push
                │                            │ (Port 754)
                │                            ▼
  ┌─────────────┴─────────┐    ┌───────────────────────────┐
  │     CLIENT NODE       │    │    REPLICA KDC SERVER     │
  │                       │    │                           │
  │  Runs: kinit / sssd   │    │   ┌───────────────────┐   │
  │  Requests Auth Tickets│    │   │    krb5-kpropd    │   │
  │  From Port 88         │    │   │ (Listens for Master)  │   │
  │                       │    │   └─────────┬─────────┘   │
  └─────────────┬─────────┘    │             │             │
                │              │             ▼ Writes      │
                └──────────────┼────────►┌───────────────┐ │
                 Auth Request  │         │ Read-Only DB  │ │
                 (Port 88)     │         └───────────────┘ │
                               │         ┌───────────────┐ │
                               │         │   krb5-kdc    │ │
                               │         │(Auth Fallback)│ │
                               │         └───────────────┘ │
                               └───────────────────────────┘
```

<!--
# Authors Notes:

Setup:
-->
