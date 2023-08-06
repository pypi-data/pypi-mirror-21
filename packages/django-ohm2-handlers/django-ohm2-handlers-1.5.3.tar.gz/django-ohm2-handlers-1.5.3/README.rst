=====
OHM2 Handlers
=====

Handlers is a complete Django app to conduct general methods and database access

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "ohm2_handlers" to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'ohm2_handlers',
      )

2. Include the handlers URLconf in your project urls.py like this::

      url(r'^ohm2_handlers/', include('ohm2_handlers.urls')),

3. Run `python manage.py migrate` to create the handlers models.

