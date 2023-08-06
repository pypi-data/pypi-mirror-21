Python ownCloud Client (pocli)
==============================

Copyright (c) 2016, 2017 Florian Kaiser, Klaus Reuter

https://gitlab.mpcdf.mpg.de/mpcdf/pocli

https://pypi.python.org/pypi/pocli

Released under the MIT License (MIT), see the LICENSE file.

Introduction
------------

The pocli package provides a lightweight ownCloud command line client
for basic file operations such as upload, download, directory creation
and listing, and deletion. It is written in Python and built upon the
official pyocclient package. 

The development of pocli was motivated by the need for a tool to quickly up- or
download single (or few) files on a computer which is operated without any
graphical user interface (i.e. a typical HPC system), and where it may not be
desirable to install the official client software. In case you have more
complex requirements (continuous synchronization), please use the official client.

A typical use case is:

* Upload a tarball from the login node of a HPC system to your ownCloud server using pocli.
* Log in to your ownCloud server from your laptop via the web browser and
  share the tarball with other users (e.g. by sending a download URL via email).

Another use case would be:

* Upload a tarball from HPC system A to your ownCloud server using pocli.
* Download the tarball to HPC system B from your ownCloud server using pocli.

Note that -- deliberately -- no recursive operations are supported.

Requirements and installation
-----------------------------

pocli was developed and tested with Python 2.7.12 and Python 3.5.2. Please drop
us a line in case pocli does not work with other (newer) Python versions.

The package including its dependencies can be installed easily via pip:

``pip install --user pocli``

Alternatively, the package can be installed from the source distribution.
First, as a requirement, pocli needs the official ownCloud Python module:

``pip install --user pyocclient``

The pocli package itself can then be installed in the standard way:

``python setup.py install --user``

Make sure to add the installation directory to the PATH environment
variable, on a Unix system this is for example "~/.local/bin". The
previous examples pass the "--user" flag in order to work purely in the
user's homedirectory. In case this flag is omitted, system-wide
locations are chosen.

Functionality examples (optional arguments are given in parentheses)
--------------------------------------------------------------------

The pocli package provides the ``oc`` command. Moreover, the alias ``ds`` can be
used interchangeably to comply with the naming of the MPCDF DataShare service.
It takes positional and named arguments in analogy to e.g. ``git``. The
following examples illustrate the basic usage:

-  basic help

``oc --help``

-  command-specific help

``oc command --help``

-  list remote files and folders, defaults to "/"

``oc ls <remote_folder>``

-  create remote directory "temp"

``oc mkdir temp``

-  upload single file to the ownCloud root directory

``oc put file1``

-  upload multiple files to the ownCloud "temp" directory

``oc put --directory=temp file1 file2 file3``

-  download single file from ownCloud to the current working directory

``oc get file1``

-  download multiple files to the local "temp" directory

``oc get --directory=temp file1 file2 file3``

-  remove remote file(s)

``oc rm file1 file2``

-  check if a connection to the server can be established successfully
   based on the present configuration

``oc check``

Under the hood
--------------

The connection to an ownCloud instance requires a valid configuration. The
configuration file in JSON format is located at "~/.ocrc" and is created at the
first invocation of the ``oc`` command. The initial default configuration is for
the MPCDF DataShare service, however, it can be configured freely to connect to
other ownCloud instances. Simply adapt the configuration file to your needs. No
credentials are ever stored in "~/.ocrc".

Password handling
-----------------

Security concerns arise in particular if the ownCloud password is
identical to the password used for other services at the same site.
To this end, by default, the ``oc`` executable asks the user to type the
password at each invocation.

..  The environment variable OC\_PASSWORD may be set to a valid password.  Bash
    users should use for security reasons the ``ocpasswd`` bash function from
    ``ocpasswd.sh`` in order to prevent the plain text password from showing up in
    the shell history. Execute the commands ``source ocpasswd.bash`` followed by
    ``ocpasswd``. Support for other shells may follow later. When using
    OC\_PASSWORD, unset it or close the shell as soon as possible after the file
    transfer operations have been done.
    In case the environment variable OC\_PASSWORD is not set the ``oc``
    command asks for the password at each invocation. For security reasons the
    authors recommend this mode of operations.
