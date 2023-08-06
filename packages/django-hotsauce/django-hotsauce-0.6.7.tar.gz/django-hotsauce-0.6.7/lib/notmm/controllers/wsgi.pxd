#!/usr/bin/env python
# Copyright (C) 2007-2014 Etienne Robillard <erob@gthcfoundation.org>
# <LICENSE=APACHE>

# BaseController C API/WSGI version:    0.5.1
# Cython version:   0.15.1/0.16

#from cython import *

cdef class BaseControllerMixIn(object):
   
    #cdef object settings, resolver, request_class, response_class
    cdef dict environ
    cdef inline application


