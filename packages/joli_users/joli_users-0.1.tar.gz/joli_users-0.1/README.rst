=====
Joli Users
=====

Joli Users is a django rest framework module for creating and managing users for mobile clients

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "joli_users" and "rest_framework.authtoken" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'joli_users',
        'rest_framework.authtoken'
    ]

2. Add these variables in settings::
  JOLI_USERS_USER_GROUP_NAME = 'example group' #eg users, mobileUsers
  JOLI_USER_PHOTOS_PATH = '/example_proj/example_path/'
  JOLI_USERS_EMAIL_SUBJECT = 'example_subject'
  JOLI_USERS_EMAIL_BODY_TEXT = 'example test'
  JOLI_USERS_EMAIL_FROM = 'example@example.com'
  JOLI_USERS_ACCOUNT_ACTIVATION_DAYS = 7

  EMAIL_HOST = 'smtp.example.com'
  EMAIL_PORT = 587
  EMAIL_USE_TLS = True

  EMAIL_HOST_USER = 'example@example.com'
  EMAIL_HOST_PASSWORD = 'example_password'

2. Include the joli_users URLconf in your project urls.py like this::

    url(r'^joli_users/', include('joli_users.urls')),

3. Run `python manage.py migrate` to create the polls models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a group (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/joli_users/ to participate in the poll.
