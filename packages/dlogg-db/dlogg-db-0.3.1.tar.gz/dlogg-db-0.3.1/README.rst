python-dlogg-db
===============

Unofficial python package to read data from a `Technische Alternative`_
`D-LOGG`_ device (using `dlogg-driver`_) and upload it to a database.


Installation
------------

.. code:: bash

  sudo apt install libmysqlclient-dev
  pip install dlogg-db


Usage
-----

.. code:: python

  from dlogg_driver import DLoggDevice
  from dlogg_db import DLoggDbUpload, DLoggDbDownload
  
  # upload
  with DLoggDevice("/dev/ttyUSB0") as device:
      with DLoggDbUpload('db-host', 3306, 'db-name', 'db-user', 'db-pw') as upload:
          upload.update_tables_format()
          upload.insert_current_data(device.get_current_data())
  
  # download
  with DLoggDbDownload('db-host', 3306, 'db-name', 'db-user', 'db-pw') as download:
    end = datetime.datetime.utcnow()
    start = end - datetime.timedelta(minutes=10)
    print download.fetch_data_range(start, end)


.. _`Technische Alternative`: http://www.ta.co.at/
.. _`D-LOGG`: http://www.ta.co.at/de/produkte/pc-anbindung/datenkonverter-d-logg.html
.. _`dlogg-driver`: https://github.com/ubruhin/python-dlogg-driver
