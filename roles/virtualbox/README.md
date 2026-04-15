# Virtualbox

[VirtualBox](https://www.virtualbox.org/) is a free, open-source hosted hypervisor developed by Oracle that allows you to run multiple operating systems (OS) simultaneously on a single physical machine.  

Setup **VirtualBox** repository and install version 7.1.

**virtualbox_selected** Options:

* virtualbox_6_1
* virtualbox_7_0
* virtualbox_7_1
* virtualbox_7_2

``` shell
$ ansible-playbook jcook3701.pkgs.virtualbox.yml -K -e "virtualbox_selected=virtualbox_7_1"
```
