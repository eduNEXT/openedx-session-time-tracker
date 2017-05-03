openedx-session-time
=============================

The ``README.rst`` file should start with a brief description of the repository.

Your project description goes here


Overview (please modify)
------------------------

The ``README.rst`` file should then provide an overview of the code in this
repository, including the main components and useful entry points for starting
to understand the code in more detail.


How to install for development purposes
---------------------------------------

In a devstack connect to the edxapp user and change into the `/edx/src/` directory.

```
sudo su edxapp
cd /edx/src/
```

Clone the repository (You can do this from outside of the vagrant VM if you want to use the local user of your system).

```
git clone git@github.com:eduNEXT/openedx-session-time-tracker.git
```

Install with the editable flag inside the virtualenv

```
cd /edx/src/openedx-session-time-tracker
pip install -e .
```

Activate the application in your django settings.
In `edx-platform/lms/envs/common.py` search for the `INSTALLED_APPS` tuple and add `openedx_session_time`.


How to create migrations for this app
-------------------------------------

In the devstack, running under the `edxapp` user and in the `~/edx-platform` directory run:

```
./manage.py lms --settings=devstack makemigrations openedx_session_time
```


How to run the management command
---------------------------------

To run the application, you need to migrate it first, and then run the `reducelogs` management command.
In the devstack, running under the `edxapp` user and in the `~/edx-platform` directory run:

```
./manage.py lms --settings=devstack makemigrations openedx_session_time
./manage.py lms --settings=devstack reducelogs
```


Documentation
-------------

The full documentation is at https://openedx-session-time-tracker.readthedocs.org.


License
-------

The code in this repository is licensed under the AGPL 3.0 unless
otherwise noted.

Please see ``LICENSE.txt`` for details.
