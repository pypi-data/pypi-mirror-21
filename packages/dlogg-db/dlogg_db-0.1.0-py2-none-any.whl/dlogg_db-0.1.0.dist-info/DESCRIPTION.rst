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
      header = device.get_header()
      data = device.fetch_data_range(header.start, header.get_sample_count())
      device.fetch_end()
      with DLoggDbUpload('db-host', 3306, 'db-name', 'db-user', 'db-pw') as upload:
              upload.create_tables()
              upload.insert_data(data)


.. _`Technische Alternative`: http://www.ta.co.at/
.. _`D-LOGG`: http://www.ta.co.at/de/produkte/pc-anbindung/datenkonverter-d-logg.html
.. _`dlogg-driver`: https://github.com/ubruhin/python-dlogg-driver


