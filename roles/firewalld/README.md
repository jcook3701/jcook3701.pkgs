# Firewalld

[Firewalld](https://firewalld.org/) provides a dynamically managed firewall with support for network/firewall zones that define the trust level of network connections or interfaces. It has support for IPv4, IPv6 firewall settings, ethernet bridges and IP sets. There is a separation of runtime and permanent configuration options. It also provides an interface for services or applications to add firewall rules directly.

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
