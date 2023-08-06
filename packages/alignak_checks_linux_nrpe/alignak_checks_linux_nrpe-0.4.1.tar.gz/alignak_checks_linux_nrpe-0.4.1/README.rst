Alignak checks package for Unix/Linux NRPE checked hosts/services
=================================================================

*Checks pack for monitoring Unix/Linux hosts with NRPE active checks*


.. image:: https://badge.fury.io/py/alignak_checks_linux_nrpe.svg
    :target: https://badge.fury.io/py/alignak-checks-linux-nrpe
    :alt: Most recent PyPi version

.. image:: https://img.shields.io/badge/IRC-%23alignak-1e72ff.svg?style=flat
    :target: http://webchat.freenode.net/?channels=%23alignak
    :alt: Join the chat #alignak on freenode.net

.. image:: https://img.shields.io/badge/License-AGPL%20v3-blue.svg
    :target: http://www.gnu.org/licenses/agpl-3.0
    :alt: License AGPL v3

Installation
------------

The installation of this checks pack will copy some configuration files in the Alignak default configuration directory (eg. */usr/local/etc/alignak*). The copied files are located in the default sub-directory used for the packs (eg. *arbiter/packs*).

From PyPI
~~~~~~~~~
To install the package from PyPI:
::

   sudo pip install alignak-checks-linux-nrpe


From source files
~~~~~~~~~~~~~~~~~
To install the package from the source files:
::

   git clone https://github.com/Alignak-monitoring-contrib/alignak-checks-linux-nrpe
   cd alignak-checks-nrpe
   sudo pip install .

**Note:** *using `sudo python setup.py install` will not correctly manage the package configuration files! The recommended way is really to use `pip`;)*

Documentation
-------------

Configuration
~~~~~~~~~~~~~

This checks pack is using the `check_nrpe` Nagios plugin that must be installed on the Alignak server running your poller daemon.

For Unix (FreeBSD), you can simply install the NRPE plugin:
::

   # Simple NRPE
   pkg install nrpe

   # NRPE with SSL
   pkg install nrpe-ssl

For Linux distros, install the Nagios ``check_nrpe`` plugin from your system repository:
::

   # Install local NRPE plugin
   sudo apt-get install nagios-nrpe-plugin
   # Note: This may install all the Nagios stuff on your machine...


After installation, the plugins are commonly installed in the */usr/local/libexec/nagios* directory.

The */usr/local/etc/alignak/arbiter/packs/resource.d/nrpe.cfg* file defines a global macro
that contains the NRPE check plugin installation path. You must edit this file to update the default path that is defined to the alignak ``$NAGIOSPLUGINSDIR$`` (defined in alignak default configuration).
::

    #-- NRPE check plugin installation directory
    # Default is to use the Alignak plugins directory
    $NRPE_PLUGINS_DIR$=$NAGIOSPLUGINSDIR$
    #--

**Note:** the default value for ``$NAGIOSPLUGINSDIR$`` is set as */usr/lib/nagios/plugins* which is the common installation directory used by the Nagios plugins.


Prepare monitored hosts
~~~~~~~~~~~~~~~~~~~~~~~

Some operations are necessary on the monitored hosts if NRPE remote access is not yet activated.
::
   # Install local NRPE server
   su -
   apt-get update
   apt-get install nagios-nrpe-server
   apt-get install nagios-plugins

   # Allow Alignak as a remote host
   vi /etc/nagios/nrpe.cfg
   =>
      allowed_hosts = X.X.X.X

   # Restart NRPE daemon
   /etc/init.d/nagios-nrpe-server start

Test remote access with the plugins files:
::
   /usr/local/var/libexec/alignak/check_nrpe -H 127.0.0.1 -t 9 -u -c check_load

**Note**: This configuration is the default Nagios NRPE daemon configuration. As such it does not allow to define arguments in the NRPE commands and, as of it, the warning / critical threshold are defined on the server side.


Alignak configuration
~~~~~~~~~~~~~~~~~~~~~

You simply have to tag the concerned hosts with the template ``linux-nrpe``.
::

    define host{
        use                     linux-nrpe
        host_name               linux_nrpe
        address                 127.0.0.1
    }



The main ``linux-nrpe`` template only declares the default NRPE commands configured on the server.
You can easily adapt the configuration defined in the ``services.cfg`` and ``commands.cfg.parse`` files.


Bugs, issues and contributing
-----------------------------

Contributions to this project are welcome and encouraged ... `issues in the project repository <https://github.com/alignak-monitoring-contrib/alignak-checks-linux-nrpe/issues>`_ are the common way to raise an information.
