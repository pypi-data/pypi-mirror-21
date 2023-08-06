===========
django-chat
===========

.. image:: https://codeclimate.com/github/tomi77/django-chat/badges/gpa.svg
   :target: https://codeclimate.com/github/tomi77/django-chat
   :alt: Code Climate
.. image:: https://travis-ci.org/tomi77/django-chat.svg?branch=master
   :target: https://travis-ci.org/tomi77/django-chat
.. image:: https://coveralls.io/repos/github/tomi77/django-chat/badge.svg?branch=master
   :target: https://coveralls.io/github/tomi77/django-chat?branch=master

A simple Django chat application

Installation
============

.. sourcecode:: sh

   pip install django-chat

Quick start
===========

Add ``chat`` to `INSTALLED_APPS`. ``django.contrib.auth`` and ``django.contrib.contenttypes`` are also required.

.. sourcecode:: python

   INSTALLED_APPS = [
       ...
       'django.contrib.contenttypes',
       'django.contrib.auth',
       'chat',
   ]

Create database

.. sourcecode:: sh

   ./manage.py migrate


