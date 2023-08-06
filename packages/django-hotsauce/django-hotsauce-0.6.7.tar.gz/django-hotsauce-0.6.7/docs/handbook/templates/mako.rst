Template Processing with Mako
==============================

:Author: Etienne Robillard <tkadm30@yandex.com>
:Version: 0.6.2
:Last modified: 2017-01-23

This is a short introduction to Unicode templates processing 
in django-hotsauce. 

Unicode Templates Processing
-----------------------------

A Unicode-aware backend is provided in the 
``notmm.utils.template.makoengine`` package. 

In short, its a simple wrapper around the Mako 
template library supporting full Unicode (UTF-8) support and caching control.

Configuration
--------------

To configure and use within a WSGI or Django app, add 
the following code to your ``development.ini`` file ::

    [template]
    template_loader = mako.CachedTemplateLoader

Further readings
-----------------

* `Mako Templates for Python <http://www.makotemplates.org/>`_
* `Introduction to ConfigObj <http://www.voidspace.org.uk/python/articles/configobj.shtml/>`_

