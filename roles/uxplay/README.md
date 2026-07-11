# UxPlay

[UxPlay](https://github.com/fdh2/uxplay) is a free, open-source AirPlay server that lets you mirror your iPhone, iPad, or Mac screen (with audio) directly to your PC. It turns your computer into an Apple TV-like receiver, making it ideal for presentations, streaming, or watching videos on a larger screen.

<!--
Authors Notes:
TODO: Firewall needs to be figured out in future for this and other apps.

Checkout: doubletake
AirPlay screen mirroring sender for Linux. Streams your desktop to an Apple TV using the AirPlay 2 mirroring protocol.

Idea for firewall tasks ->

# UFW Task Block
- name: Configure UFW rules for UxPlay
  community.general.ufw:
    rule: allow
    port: "{{ item.port | string }}"
    proto: "{{ item.proto }}"
    comment: "{{ item.comment }}"
  loop: "{{ uxplay_firewall_rules }}"
  when:
    - uxplay_manage_firewall | bool
    - uxplay_firewall_backend == 'ufw'

# Firewalld Task Block (Example of swapping backends easily)
- name: Configure Firewalld rules for UxPlay
  ansible.posix.firewalld:
    port: "{{ item.port }}/{{ item.proto }}"
    zone: public
    state: enabled
    permanent: true
    immediate: true
  loop: "{{ uxplay_firewall_rules }}"
  when:
    - uxplay_manage_firewall | bool
    - uxplay_firewall_backend == 'firewalld'

-->
