========
HexOmega
========

HexOmega is a simple, turn-key task management django app written for 
Murdoch University. 

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "users" and "log" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'users',
        'log',
    ]

2. Include the users URLconf in your project urls.py like this::

    url(r'', include('users.urls')),

3. Run `python manage.py migrate` to create the users models.

4. Run `python manage.py setup_init` to create default users and the roles table.