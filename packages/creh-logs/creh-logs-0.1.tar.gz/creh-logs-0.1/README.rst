=====
Creh Logs
=====

Creh-logs is a simple Django app to conduct Web-based polls. For each
question, visitors can choose between a fixed number of answers.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "polls" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'logs',
    ]

2. Run "python manage.py migrate" to create the log models.
