ACS-CLI
=======

What is it?
-----------

A command line tool for accessing Alfresco Content Services repository
servers through the public REST APIs.

The motivation for building this tool is two-fold: firstly as an
interesting way for me to learn python; and secondly it's the tool I
always wish existed. The code probably isn't very *pythonic* or well
organised, but hopefully this will get better :-)

Installation
------------

Use (python3) pip to install:

::

    pip3 install acs-cli

To try this out in docker with a self-destructing temporary container:

::

    mward@holly:~$ docker run -it --rm ubuntu:16.04
    root@f957e9b7154f:/# apt update && apt install -y python3 python3-pip
    root@f957e9b7154f:/# pip3 install acs-cli

If you are running the ACS instance on the main host, then get the IP
address of the appropriate interface, e.g. on Macbook: ``ifconfig en0``
for my wifi IP address.

Warning
-------

This is a proof of concept and must be considered *alpha* quality
software at best.

Example usage
-------------

Without any arguments, you may log in to http://localhost:8080/alfresco
using the username 'admin' and will be prompted for a password.

::

    mward@holly:~$ acs login
    Logging in admin to http://localhost:8080/alfresco
    Password:
    mward@holly:acs-cli$

Use the ``--username`` or ``--password`` options to log in with
different credentials:

::

    mward@holly:~$ acs login --username=asmith --password=ban4n4@!

Once logged in, APIs may be exercised by using the general format:

::

    acs <api or command> <subcommand> [options...] <arguments...>

or by invoking python explicitly:

::

    python3 acs.py <api or command> <subcommand> [options...] <arguments...>

Here we see the people API being used to create a person entity:

::

    mward@holly:~$ acs people create-person asmith ban4n4@! asmith@example.com Alison
    {
        "entry": {
            "firstName": "Alison",
            "id": "asmith",
            "emailNotificationsEnabled": true,
            "email": "asmith@example.com",
            "enabled": true,
            "company": {}
        }
    }

All API operations accept the ``--query`` option to specify a JMESPath
expression. Here for example, we choose to only display the ``id`` and
``email`` fields of the returned ``entry`` object:

::

    mward@holly:~$ acs people get-person jbloggs --query 'entry.[id,email]'
    [
        "jbloggs",
        "jbloggs@example.com"
    ]

And here, we use the ``--query`` option to view ``id``, ``firstName``
and ``email`` of *each* entry in the list of people:

::

    mward@holly:~$ acs people list-people --query='list.entries[].entry.[id,firstName,email]'
    [
        [
            "admin",
            "Administrator",
            "admin@alfresco.com"
        ],
        [
            "guest",
            "Guest",
            null
        ],
        [
            "jbloggs",
            "Joe",
            "jbloggs@example.com"
        ]
    ]

Any *list* operation that may be paged can be used with the
``--max-items`` and ``--skip-count`` options, used here to show two
results after skipping the first 4. This may be thought of as showing
the *third* page of results.

::

    mward@holly:~$ acs people list-people --query='list.entries[].entry.[firstName]' --max-items=2 --skip-count=4
    [
        [
            "Joe10"
        ],
        [
            "Joe11"
        ]
    ]

The *sites* API may be used to list "sites" as used extensively in the
Share application. This is a paged API and here we use it without the
``--max-items`` and ``--skip-count`` options which default to 10 and 0
respectively:

::

    mward@holly:~$ acs sites list-sites --query='list.entries[].entry'
    [
        {
            "title": "accounts",
            "role": "SiteManager",
            "guid": "80dbd63c-3dbf-4005-bd16-e324fa8b4517",
            "id": "accounts",
            "visibility": "PUBLIC",
            "preset": "site-dashboard"
        },
        {
            "title": "Sample: Web Site Design Project",
            "guid": "b4cff62a-664d-4d45-9302-98723eac1319",
            "id": "swsdp",
            "visibility": "PUBLIC",
            "description": "This is a Sample Alfresco Team site.",
            "preset": "site-dashboard"
        }
    ]


