========
VISA Web
========

Polls is a simple Django app to conduct Web-based VISA interface. Execute and log VISA operations.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "visaweb" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'visaweb',
    ]

2. Include the visaweb URLconf in your project urls.py like this::

    url(r'^polls/', include('polls.urls')),

3. Run `python3 manage.py migrate` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a VISA alias (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/visaweb/ to participate in the poll.