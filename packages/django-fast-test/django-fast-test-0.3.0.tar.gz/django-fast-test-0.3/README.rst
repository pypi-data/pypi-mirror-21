django-fast-test
=================

**django-fast-test** provides a Django Command fast_test.


Features
--------

- Django fast_test command.


Installation & Usage
--------------------

1. Install from code using ``python setup.py build`` and then ``python setup.py install``, or using ``pip install django-fast-test``.
2. Add ``'django_fast_storage'`` to your ``INSTALLED_APPS`` setting.
3. Run the command by: ``python manage.py fast_test``.


How it works
------------

The fast_test command runs very fast, because it does not create TEST DB and does not run migrations.
Directly, it uses the developing db or product db, and the result of operations onto db is really durably committed.
So, CAUTIOUSLY use this command.


Support and announcements
-------------------------

Downloads and bug tracking can be found at the `main project
website <http://github.com/liumengjun/django-fast-test>`_.
