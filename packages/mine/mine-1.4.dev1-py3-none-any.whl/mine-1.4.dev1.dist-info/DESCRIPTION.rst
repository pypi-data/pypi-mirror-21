...for applications that haven't learned to share.

| |Build Status|
| |Coverage Status|
| |Scrutinizer Code Quality|
| |PyPI Version|
| |PyPI Downloads|

Overview
========

This program lets you synchronize application data using Dropbox.

It automatically starts and stops programs that would otherwise fight
over data in a shared folder and ensures only one instance is running.
Many applications work fine when their data is stored in Dropbox, but
some programs overwrite databases:

-  iTunes
-  iPhoto
-  etc.

while others periodically write snapshot data:

-  Eclipse
-  Xcode
-  etc.

and some just don't make sense to keep running on all your computers:

-  Slack
-  HipChat
-  etc.

Setup
=====

Requirements
------------

-  Python 3.3+

Installation
------------

Install mine with pip:

.. code:: sh

    $ pip install mine

or directly from the source code:

.. code:: sh

    $ git clone https://github.com/jacebrowning/mine.git
    $ cd mine
    $ python setup.py install

Configuration
-------------

Create a ``mine.yml`` in your Dropbox:

.. code:: yaml

    config:
      computers:
      - name: My iMac
        hostname: My-iMac.local
        address: 00:11:22:33:44:55
      - name: My MacBook Air
        hostname: My-MacBook-Air.local
        address: AA:BB:CC:DD:EE:FF
      applications:
      - name: iTunes
        properties:
          auto_queue: false
          single_instance: true
        versions:
          mac: iTunes.app
          windows: iTunes.exe
          linux: null
      - name: Slack
        properties:
          auto_queue: true
          single_instance: false
        versions:
          mac: Slack.app
          windows: null
          linux: null

Include the applications you would like ``mine`` to manage. Computers
are added automatically when ``mine`` is run.

The ``versions`` dictionary identifies the name of the executable on
each platform. The ``properties.auto_queue`` setting indicates ``mine``
should attempt to launch the application automatically when switching
computers. The ``properties.single_instance`` setting indicates the
application must be closed on other computers before another instance
can start.

Usage
=====

To synchronize the current computer's state:

.. code:: sh

    $ mine

To close applications on remote computers and start them locally:

.. code:: sh

    $ mine switch

To close applications running locally:

.. code:: sh

    $ mine close

To close applications locally and start them on another computer:

.. code:: sh

    $ mine switch <name>

To delete conflicted files in your Dropbox:

.. code:: sh

    $ mine clean

.. |Build Status| image:: http://img.shields.io/travis/jacebrowning/mine/master.svg
   :target: https://travis-ci.org/jacebrowning/mine
.. |Coverage Status| image:: http://img.shields.io/coveralls/jacebrowning/mine/master.svg
   :target: https://coveralls.io/r/jacebrowning/mine
.. |Scrutinizer Code Quality| image:: http://img.shields.io/scrutinizer/g/jacebrowning/mine.svg
   :target: https://scrutinizer-ci.com/g/jacebrowning/mine/?branch=master
.. |PyPI Version| image:: http://img.shields.io/pypi/v/mine.svg
   :target: https://pypi.python.org/pypi/mine
.. |PyPI Downloads| image:: http://img.shields.io/pypi/dm/mine.svg
   :target: https://pypi.python.org/pypi/mine

Revision History
================

1.3 (2017/03/13)
----------------

-  Ignored conflicting program name ("iTunes Helper.app").

1.2 (2017/02/13)
----------------

-  Restart Dropbox automatically.

1.1 (2017/01/07)
----------------

-  Updated ``switch`` to close all locally running applications.

1.0 (2016/11/01)
----------------

-  Initial stable release.

0.6.1 (2016/09/23)
------------------

-  Added a delay to ensure all applications close.
-  Fixed cleanup of unused applications and computers.

0.6 (2016/07/02)
----------------

-  Added a ``close`` command to close all locally running applications.

0.5 (2016/05/16)
----------------

-  Added periodic checking to the daemon (regardless of file changes).

0.4.3 (2016/05/11)
------------------

-  Fixed ``__init__`` warnings with YORM v0.8.1.

0.4.2 (2016/03/30)
------------------

-  Updated to YORM v0.7.2.

0.4.1 (2016/02/23)
------------------

-  Updated to YORM v0.6.

0.4 (2015/12/30)
----------------

-  Added file watching to update program state faster.

0.3 (2015/11/14)
----------------

-  Added automatic daemon restart using ``nohup``.
-  Moved ``queued`` to setting ``properties.single_instance``.
-  Added ``properties.auto_queue`` to filter active applications.

0.2.1 (2015/09/05)
------------------

-  Fixed daemon warning to run using ``nohup``

0.2 (2015/08/27)
----------------

-  Added ``--daemon`` option to run continuously.
-  Added ``edit`` command to launch the settings file.

0.1.2 (2015/05/17)
------------------

-  Updated to YORM v0.4.

0.1.1 (2015/03/19)
------------------

-  Initial release.


