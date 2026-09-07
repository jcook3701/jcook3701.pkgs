# Mutt

[Mutt](http://www.mutt.org/) is a powerful, highly customizable, text-based email client for Linux and other Unix-like systems, primarily controlled by the keyboard. It is designed for power users who prefer working within a command-line environment and is well-known for its speed and security focus.

Install **Mutt** email client.

``` shell
$ ansible-playbook jcook3701.pkgs.mutt.yml -K
```

Uninstall **Mutt** email client.

``` shell
$ ansible-playbook jcook3701.pkgs.mutt.yml -K -e "mutt_state=absent"
```

## Author Information

Maintained by **Jared Cook** as part of the core infrastructure and container management ecosystem.

<!--
# TODO:
    * Fix up muttrc file to ensure won't fail if missing values.
    * Add all values called in muttrc file to either defaults/main.yml or
      vars/main.yml.
-->
