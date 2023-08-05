ldapmgk
=======

*Helper for managing an LDAP directory on CLI*

Purpose
-------

ldapmgk is a simple command line program that manages an LDAP directory. You
can use it to easily add or remove users and groups, reset passwords and 
add or remove users to groups.

Requirements
------------

This program requires openldap development files for using the `python-ldap`
module. It'll be needed wheh installing through `pip`.

Installation
------------

Using pip, it should be easy::

    $ pip install ldapmgk

If you're not using pip or got it from the repository, use the following
command::

    $ pip install -e .

We recommend using virtualenv to setup a self-contained app directory. In this
case, you should use::

    $ virtualenv env
    $ source env/bin/activate
    $ pip install -e .

If you want to see which libraries this application uses, please check the
``requirements.txt`` file.

Usage
-----

Default paths:

- Configuration: */etc/ldapmgk/ldapmgk.cfg*

To run it, activate virtualenv first::

    $ source env/bin/activate
    $ ldapmgk -h
