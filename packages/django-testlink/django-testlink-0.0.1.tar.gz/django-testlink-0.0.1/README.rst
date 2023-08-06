=====
Django Testlink
=====
A Django app to integrate php testlink 1.9.16 into Django system.

Detailed documentation is in the "docs" directory.
Quick start
-----------

1. Add "django-testlink" to your INSTALLED_APPS setting like this::
   INSTALLED_APPS = [
   ...
   'django-testlink', ]

2. Include the polls URLconf in your project urls.py like this::
   url(r'^testlink/', include('testlink.urls')),

3. Run `python manage.py migrate` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
         to use testlink (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/testlink/ to participate in the poll.

