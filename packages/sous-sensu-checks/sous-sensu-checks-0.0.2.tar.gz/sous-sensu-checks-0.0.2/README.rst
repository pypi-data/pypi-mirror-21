sous-sensu-checks
==================
Calls otpl-service-check for each compatible deployment found in a sous
global deploy manifest (GDM).

Writes the results of these checks to the local Sensu client.

Usage
-----
This script should be run on a schedule to re-write a file in
``/etc/sensu/conf.d/checks``.

Dependencies
------------
See ``requirements.txt``.

Arguments
---------
Run with ``-h`` or ``--help`` to see command-line argument
documentation.

