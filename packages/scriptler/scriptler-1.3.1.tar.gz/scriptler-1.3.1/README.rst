scriptler
=========

.. image:: https://travis-ci.org/AFriemann/scriptler.svg?branch=master
    :target: https://travis-ci.org/AFriemann/scriptler
.. image:: https://badge.fury.io/py/scriptler.svg
    :target: https://badge.fury.io/py/scriptler

Scriptler allows you to manage scripts from different sources in one place with a simple configuration file.

installation
------------

As usual, use pip to install::

    $ pip install --user scriptler

usage
-----

First off, create a configuration file in ~/.config/scriptler/config.yml::

    scriptler:
        script_dir: /home/aljosha/.local/share/scriptler

    scripts:
        proxy-foxy:
            path: ~/git/scripts/bash/proxy-foxy
        socksme:
            path: ~/git/scripts/bash/socksme
        swap:
            path: bash/swap
            source: afriemann/scripts.git
        h:
            source: hhighlighter
            path: h.sh
            command: echo 'h $@' >> {}

    sources:
        afriemann/scripts.git:
            branch: master
            url: github.com/AFriemann/scripts
        hhighlighter:
            url: github.com/paoloantinori/hhighlighter
            branch: master

Repository sections may be named however you please while script sections will determine the linked filename.
The command can be used to run commands after script installation. *{}* expands to the file. In this particular example it will
add "h" to the file since it normally only contains a function called "h".
The *scriptler* section is not required (~/.local/share/scriptler is the default) but *script_dir* should be something you have
write access to and can add to your $PATH.

To install the scripts, simply run::

    $ scriptler update
    installing socksme
    installing swap
    installing proxy-foxy
    installing h
    removing unmanaged file foobar

This will also remove unmanaged files (those that you removed from your configuration file/never added).

And to remove them again::

    $ scriptler remove
    removing swap
    removing proxy-foxy
    removing socksme
    removing h

To get a nice list of currently installed scripts::

    $ scriptler status
    config file  ~/.config/scriptler/config
    script dir   ~/.local/share/scriptler

    script     managed    installed
    ---------  ---------  -----------
    swap       yes        no
    h          yes        yes
    proxy-foxy yes        yes
    socksme    yes        yes
    foobar     no         yes

todo
----

* scriptler will ruthlessly reinstall files. Right now I don't care, but it would probably be better to change that
* the only sources supported right now are github and local files
* write some tests to ensure functionality
* *scriptler config edit* should not parse the config file beforehand and should check afterwards
* the command option for sources is very rudimentary and probably asking for tons of problems

license
-------

"THE BEER-WARE LICENSE" (Revision 42)::

    <aljosha.friemann@gmail.com> wrote this file.  As long as you retain this
    notice you can do whatever you want with this stuff. If we meet some day,
    and you think this stuff is worth it, you can buy me a beer in return.

