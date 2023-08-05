Juju Virtual Network Function Manager
=====================================

This project is a Virtual Network Function Manager (VNFM) that enables
`Juju`_ to work as a VNFM in the `Open Baton`_ environment.

Requirements
------------

-  Python 3.5.2+
-  Juju 2.0+

Installation
------------

For installing the Juju-VNFM execute

.. code:: bash

    pip install .

inside the project’s root directory. **Note** that you have to use pip3 if
your standard Python interpreter is python2.

Usage
-----

After you installed the Juju-VNFM you have to configure it. Create the
file */etc/openbaton/juju/conf.ini*, make sure that the current user has write permissions for the file and execute:

.. code:: bash

    jujuvnfm configure

Then follow the instructions.

Afterwards you can start the Juju-VNFM with the command *jujuvnfm
start*. You can specify the number of threads started to handle NFVO
requests by passing a number with the -t option:

.. code:: bash

    jujuvnfm -t 10 start

The default number of threads is five.

.. _Juju: https://jujucharms.com/
.. _Open Baton: https://openbaton.github.io/
