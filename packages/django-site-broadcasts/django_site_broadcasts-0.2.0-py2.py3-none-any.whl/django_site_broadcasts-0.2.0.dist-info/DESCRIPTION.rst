======================
django-site-broadcasts
======================

The site broadcast application allows users to define short messages and
announcements that should be displayed across a site.

Each broadcast message consists of a short message, an optional start time, and
a completion time, when the should be displayed across a site.

Installation
============

Use pip:

    pip install django-site-broadcasts

Or clone the repository and use the ``setup.py`` file to install the application.

    python setup.py install

Then add ``broadcasts`` to your ``INSTALLED_APPS`` and
``broadcasts.context_processors.broadcast_message`` to
``TEMPLATE_CONTEXT_PROCESSORS``.

Usage
=====

If you've added the context processor to your list of context processors, you
can simply refer to the current message using the context variable::

    {{ broadcast_message }}

The message itself should be displayed with::

    {{ broadcast_message.message }}

TO-DO
=====

* Handle time zones (Django project timezone may differ from server timezone)
* Use caching (if available)




History
=======

0.1.1
-----

* Fix an installation bug

0.1.0
-----

* Django 1.7+ compatibility (moved South migrations module to `south_migrations`
  and added native Django `migrations` module - thanks to @smajda for that)

0.0.1
-----

* First release


