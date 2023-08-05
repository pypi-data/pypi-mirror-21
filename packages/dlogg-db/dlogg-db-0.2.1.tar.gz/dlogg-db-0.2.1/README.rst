python-dlogg-db
===============

Unofficial python package to read data from a `Technische Alternative`_
`D-LOGG`_ device (using `dlogg-driver`_) and upload it to a database.


Installation
------------

.. code:: bash

  pip install dlogg-db


Usage
-----

.. code:: python

  from dlogg_driver import DLoggDevice
  from dlogg_db import DLoggDbUpload
  
  with DLoggDevice("/dev/ttyUSB0") as device:
      with DLoggDbUpload('db-host', 3306, 'db-name', 'db-user', 'db-pw') as upload:
          upload.update_tables_format()
          upload.insert_current_data(device.get_current_data())


.. _`Technische Alternative`: http://www.ta.co.at/
.. _`D-LOGG`: http://www.ta.co.at/de/produkte/pc-anbindung/datenkonverter-d-logg.html
.. _`dlogg-driver`: https://github.com/ubruhin/python-dlogg-driver
