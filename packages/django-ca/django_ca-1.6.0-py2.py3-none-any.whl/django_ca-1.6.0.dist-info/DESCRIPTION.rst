django-ca is a tool to manage TLS certificate authorities and easily issue and revoke
certificates. It is based `cryptography <https://cryptography.io/>`_ and `Django
<https://www.djangoproject.com/>`_. It can be used as an app in an existing Django project or stand-alone with
the basic project included.  Everything can be managed via the command line via `manage.py` commands - so no
webserver is needed, if you’re happy with the command-line.

Features:

* Set up a secure local certificate authority in just a few minutes.
* Written in Python 2.7/Python3.4+, requires Django 1.8 or later.
* Manage your entire certificate authority from the command line and/or via Djangos admin
  interface.
* Get email notifications about certificates about to expire.
* Certificate validation using Certificate Revocation Lists (CRLs) and via an included OCSP
  responder.

Please see https://django-ca.readthedocs.org for more extensive documentation.


