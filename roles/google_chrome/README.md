# Google Chrome

Chrome is the official web browser from Google, built to be fast, secure, and customizable. Download now and make it yours.

## Role Variables

| Variable | Type | Description / Choices | Default |
| :--- | :--- | :--- | :--- |
| **`google_chrome_state`** | `str` | The desired lifecycle state of Google Chrome on the managed system.<br>• `present`<br>• `absent`<br>• `latest` | `"present"` |
| **`google_chrome_base_repo_url`** | `str` | The base URL for the official Google Chrome package repository. | `"https://google.com"` |

## Author Information

Maintained by **Jared Cook** as part of the core infrastructure and container management ecosystem.
