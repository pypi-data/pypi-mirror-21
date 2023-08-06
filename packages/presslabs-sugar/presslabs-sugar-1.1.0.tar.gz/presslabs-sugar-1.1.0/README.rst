=====
Sugar
=====

Various sugars and goodies for projects. They are mainly for Presslabs
internal use, but can be proven usefull for any other projects.

Use as django app
-----------------

To use sugar in your django app, add "pl_sugar" to your INSTALLED_APPS setting
before django.contrib.admin::

    INSTALLED_APPS = [
        ...
        'pl_sugar',
        'django.contrib.admin',
        ...
    ]


It provides the folowing goodies:

1. Admin filters with more than 5 items are dropdowns
2. Adds header pagination for django rest framework in :code:`pl_sugar.rest_framework.pagination.LinkHeaderPagination`
3. If you install social-auth it displays the Google Login button on admin login page. Also it provides
   :code:`pl_sugar.social_auth.pipeline.set_admin_perms` which sets as super admins users defined in
   :code:`SOCIAL_AUTH_ADMIN_EMAILS`
