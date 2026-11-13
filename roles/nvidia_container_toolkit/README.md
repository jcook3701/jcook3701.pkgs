# Nvidia Container Toolkit

The [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/docker-specialized.html) is the current framework used to build and run GPU-accelerated containers. It integrates directly with container runtimes (such as Docker, Podman, containerd, and LXC) rather than wrapping around them.

* Architecture: It injects a custom runtime hook (nvidia-container-runtime-hook) into the container lifecycle. This automatically exposes host GPU devices and drivers to the container without requiring driver installation inside the image.  
* Component Split: The library separates the low-level CLI utilities (libnvidia-container) from the high-level configuration engine (nvidia-container-toolkit), allowing cross-runtime support.  
* Runtime Support: It configures Docker daemon specifications (daemon.json) or containerd configurations to add nvidia as an available low-level OCI runtime handler.  

## Role Variables

| Variable | Type | Description / Choices | Default |
| :--- | :--- | :--- | :--- |
| `nvidia_container_toolkit_state` | `str` | Desired lifecycle state. Choices: `present`, `absent`, `teardown` | `present` |
| `nvidia_container_toolkit_download_url` | `str` | Base URL used for NVIDIA Container Toolkit downloads. | `https://nvidia.github.io` |

## Author Information

Maintained by **Jared Cook** as part of the core infrastructure and container management ecosystem.
