serapeum.backup
===============

*serapeum.backup* will perform a back-up of a list of directories, as
well as your MySQL database, and store them on the server you're running
the application on. It is designed to run on your back-up server and
uses ```rdiff-backup`` <http://www.nongnu.org/rdiff-backup/>`__ to run
the backup.

Configuration
-------------

The application is designed to be used when you have a lot of servers,
which contain mostly web applications, with assorted databases, and you
want them all backed up hassle-free to a remote backup server. It is
meant to be used on your backup server, but it can optionally run from
your server and push to the backup server as well.

All configuration options are in either in ``/etc/serapeum/backup.ini``
or a configuration file provided via the ``--config`` command line
switch. Copy the provided ``example.ini`` file and update it to reflect
your personal situation.

Role
~~~~

The setting ``remote_role`` determines whether *serapeum.backup* will
attempt to backup servers to the local system (``source``) or backup the
local system to some remote server (``backup``). By default, it's set to
``source``.

-  Setting it to ``backup`` will create a backup of the local system and
   use the remote (hence the term ``remote_role``) as its backup
   location.

-  Setting it to ``source`` will create a backup of the remote system
   and store the backup locally.

The key ``backup_path`` contains the path the backups will be written
to, either a local path (``source``) or a remote (``backup``) one.

Note that when ``remote_role`` is ``backup`` and thus ``backup_path`` is
a remote path, you do not have to include ``user`` and ``host`` (e.g.
``user@host::path``), as this will be generated automatically from the
remote configuration.

File selection
~~~~~~~~~~~~~~

``sources_file`` and ``excludes_file`` refer to the selection of files
(or directories) you want to backup. Both files must be json-files which
have a key called ``list``. The ``list`` key contains a list of fully
qualified directories to backup.

-  ``sources_file`` contains a list of directories or files you want to
   have backed up.

-  ``excludes_file`` has a list of files or directories inside your
   source directories you want to exclude from backing up. If, for
   example, you have ``/home/pieter`` in your ``sources_file``, but want
   to exclude *LargeDir* from the backup, you specify
   ``/home/pieter/LargeDir`` inside your ``excludes_file``.

Your entire path will be replicated inside your backup location. If you
specified ``/home/pieter`` inside ``sources_file`` your remote location
will contain ``/home/pieter`` (and not just ``pieter``, which some
applications might do).

Remote configuration
~~~~~~~~~~~~~~~~~~~~

The application interacts with your remote backup server using
rdiff-backup and ssh keys. You must have rdiff-backup installed on the
remote server as well as locally, inside ``/usr/bin``. You must also
have a user that is allowed to connect via ssh, with a key, and has the
necessary rights to run ``/usr/bin/rdiff-backup`` as ``sudo`` without a
password.

-  ``remote_user``, ``remote_ssh`` and ``remote_loc`` configure the
   remote. ``remote_loc`` contains the address (IP or FQDN) of your
   remote system. ``user`` and ``ssh`` refer to the user you want to log
   in as and the location of the private ssh key on this system.

Multiple remotes
^^^^^^^^^^^^^^^^

It is possible to define multiple remotes, which will, depending on the
setting of ``remote_role``, be used to store your backups (*backup*) or
be backed up (*source*). The remotes must be in a file in JSON-format
with a key called ``list``, containing either the IP addresses or the
FQDN of every remote.

You must specify the location of the list as the ``remote_list``
parameter and remove the ``remote_loc`` key. Only one of those can
appear in your configuration file.

If the ``remote_role`` is *source*, the script will create a
subdirectory inside ``backup_path`` for every remote (using the IP/FQDN
as defined in the list), in which the backups will be stored. This
should prevent backup mix-ups.

The ``remote_``-configuration in the MySQL section has the same
functionality and is configured in the same manner.

MySQL configuration
~~~~~~~~~~~~~~~~~~~

Backing up a MySQL installation can be enabled or disabled through the
``backup_mysql`` setting.

The application uses the ``mysqldump`` utility to perform backups of
your MySQL (or equivalent) server. All databases will be dumped and the
dump will be stored locally and then transferred to the remote location
using rdiff-backup. The local copy will be deleted (for security
reasons).

-  ``local_path`` is the directory the dump will be stored in. This
   directory must exist. Not that this can be a path on a remote system
   if ``remote_role`` is set to ``source``.

-  ``host``, ``username`` and ``password`` must refer to a user that has
   the necessary rights to execute a dump of the entire MySQL
   installation. This requires ``SELECT``, ``LOCK TABLES``,
   ``SHOW VIEW`` and ``RELOAD`` privileges on all databases.

-  ``remote_user``, ``remote_ssh``, ``remote_loc``/``remote_list`` and
   ``backup_path`` are used to configure rdiff-backup for the backup of
   the MySQL dump. They can be the same settings as for the back-up of
   your files (see *Remote configuration*), but this is not a
   requirement.

Email configuration
~~~~~~~~~~~~~~~~~~~

When a backup job fails, the application sends of an email with the
output of rdiff-backup or mysqldump.

-  ``mail_dest`` has the email address of the recipient (e.g. you).

-  ``smtp_server``, ``smtp_port``, ``smtp_username`` and
   ``smtp_password`` configure the connection to a SMTP server.

Usage
-----

This script is designed to run in a cron job without any intervention.
All settings must be set in the configuration file.

Run the application as:

::

    serapeum-backup

Optionally, you can provide a configuration file (in the same format as
``/etc/serapeum/backup.ini``) on the command line via the ``--config``
or ``-c`` switch. This file will be used instead of the general
configuration file.

::

    serapeum-backup --config /etc/serapeum/specific_site.ini
