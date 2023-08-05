#########
PyQtTango
#########

.. image:: https://badge.fury.io/py/pyqttango.svg
   :target: http://badge.fury.io/py/pyqttango

Provides a Qt resource file containing Tango freedesktop.org icons.

Installation
============

Using pip::

    pip install pyqttango

In your code,::

    import pyqttango

You can then use the `fromTheme(name) <http://doc.qt.io/qt-5/qicon.html#fromTheme>`_
command of `QIcon <http://doc.qt.io/qt-5/qicon.html>`_ to get Tango icons. 
For example::

    import sys
    import pyqttango
    from PyQt5 import QtGui

    app = QtGui.QGuiApplication(sys.argv) # Only necessary if an application is not already created
    icon = QtGui.QIcon.fromTheme('accessories-calculator')
    
For the possible icon names, please refer to the freedesktop.org 
`Icon Naming Specification <https://specifications.freedesktop.org/icon-naming-spec/icon-naming-spec-latest.html>`_
or `WikiMedia Commons <https://commons.wikimedia.org/wiki/Tango_icons>`_.

Development
===========

*pyqttango* generates the Qt resource file (``.rcc``) using all SVG images available on
`WikiMedia Commons <https://commons.wikimedia.org/wiki/Tango_icons>`_.
The resource file is distributed as part of the wheel.
If you want to manually create it, run::

    python3 setup.py generate_rcc
    
License
-------

License under the GNU GPL v3, as PyQt5.

Copyright (c) 2017 Philippe Pinard

    