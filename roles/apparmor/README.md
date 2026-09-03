# Apparmor

AppArmor is an effective and easy-to-use Linux application security system. AppArmor proactively protects the operating system and applications from external or internal threats, even zero-day attacks, by enforcing good behavior and preventing both known and unknown application flaws from being exploited.

**Install:**
``` shell
$ ansible-playbook jcook3701.pkgs.apparmor.yml -K
```

**Uninstall:**
``` shell
$ ansible-playbook jcook3701.pkgs.apparmor.yml -K -e "apparmor_state=absent"
```

## Author Information

Maintained by **Jared Cook** as part of the core infrastructure and container management ecosystem.
