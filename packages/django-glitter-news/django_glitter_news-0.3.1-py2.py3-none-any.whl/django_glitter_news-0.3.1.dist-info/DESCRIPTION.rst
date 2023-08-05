===================
Django Glitter News
===================


Django glitter news for Django.


Installation
============


Getting the code
----------------

You can get **django-glitter-news** by using **pip**:

.. code-block:: console

    $ pip install django-glitter-news

Prerequisites
-------------

Make sure you add ``'glitter_news'``, ``'taggit'`` and ``'adminsortable'`` to your
``INSTALLED_APPS`` setting:

.. code-block:: python

    INSTALLED_APPS = [
        # ...
        'glitter_news',
        'taggit',
        'adminsortable',
        # ...
    ]

URLconf
-------

Add the Glitter News URLs to your project’s URLconf as follows:


.. code-block:: python

    url(r'^news/', include('glitter_news.urls', namespace='glitter-news'))


Configuration
=============

The django-glitter-news provides just one setting that you can enable in your
project.

GLITTER_NEWS_TAGS
-----------------

Default: ``False``

This setting enables tags for the model ``Post`` in your project.


