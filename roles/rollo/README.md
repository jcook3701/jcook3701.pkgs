# Rollo Printers - Linux Drivers

[Rollo](https://www.rollo.com/) printer drivers for [Linux](https://www.rollo.com/driver-linux/)

Install **Rollo Driver** package from vender website.

``` shell
$ ansible-playbook jcook3701.pkgs.rollo.yml -K
```

Uninstall **Rollo Driver** package from vender website.

``` shell
$ ansible-playbook jcook3701.pkgs.rollo.yml -K -e "rollo_state=absent"
```

## Author Information

Maintained by **Jared Cook** as part of the core infrastructure and container management ecosystem.

<!--
# TODO:
- name: Discover the dynamic physical USB device node for Rollo hardware
  # Maps the hardware ID '09c5' to its active /dev/usb/lpX system endpoint
  ansible.builtin.shell: >-
    grep -l "09c5" /sys/class/usb_device/*/device/idVendor |
    head -n 1 |
    awk -F/ '{print $5}' |
    xargs -I {} lscgroup 2>/dev/null |
    cat /sys/class/usb_device/*/device/../lp* 2>/dev/null |
    grep -o 'lp[0-9]' ||
    ls -l /dev/usb/lp* 2>/dev/null | grep 'lp' | awk '{print $NF}' | xargs basename
  register: active_rollo_dev_node
  failed_when: false
  changed_when: false

- name: Set fallback device node if discovery fails
  ansible.builtin.set_fact:
    rollo_node: "{{ active_rollo_dev_node.stdout | default('lp1') | trim }}"

- name: Query current CUPS device path mapping status
  ansible.builtin.command: >-
    lpstat -v "{{ rollo_printer_name }}"
  register: existing_device_map
  failed_when: false
  changed_when: false

- name: Attach physical USB device path mapping profiles inside CUPS backend
  ansible.builtin.command: >-
    lpadmin -p "{{ rollo_printer_name }}"
    -E
    -v "usb://dev/usb/{{ rollo_node }}"
    -m rollo-x1038.ppd
    -L "{{ rollo_printer_location }}"
    -o color-model-device-type=none
  when: existing_device_map.rc != 0 or rollo_node not in existing_device_map.stdout
  changed_when: true
  notify: "Restart CUPS"

- name: Force default paper size parameters to 4x6 thermal labels
  ansible.builtin.command: >-
    lpadmin -p "{{ rollo_printer_name }}"
    -o media=Custom.4.00x6.00in
    -o PageSize=Custom.4.00x6.00in
  changed_when: true

- name: Ensure the print queue is explicitly enabled and accepting jobs
  ansible.builtin.command: >-
    cupsenable "{{ rollo_printer_name }}" && cupsaccept "{{ rollo_printer_name }}"
  changed_when: false
--->
