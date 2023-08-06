===================
django-oss2-storage
===================

Installation
============
Installing from PyPI is as easy as doing::

  pip install django-oss2-storage

Once that is done add ``storages`` to your ``INSTALLED_APPS`` and set ``DEFAULT_FILE_STORAGE`` to the
backend of your choice. If, for example, you want to use the boto3 backend you would set::

  DEFAULT_FILE_STORAGE = 'oss2_storage.backends.Oss2MediaStorage'

