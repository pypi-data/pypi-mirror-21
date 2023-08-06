#!/usr/bin/env python
"""Base model classes for django-hotsauce"""
import logging
import schevo.mt

log = logging.getLogger(__name__)
from notmm.dbapi.orm.model cimport ModelBase
from notmm.dbapi.orm import RelationProxy
from notmm.utils.django_settings import LazySettings

from management.commands import introspect

_settings = LazySettings()
_installed_models = []

__all__ = ('Model', 'ModelManager', 'populate', 'setup', 'get_models')

def get_models():
    return _installed_models

def setup():
    populate()

def populate(verbose=False):
    """Populate _installed_models with the list of configured models"""
    for app in _settings.INSTALLED_APPS:
        if verbose:
            log.debug("Configuring %s" % app)
        app_info = introspect.by_module_name(app)
        _installed_models.append(app_info)

class Model(ModelBase):

    initialized = False
    multithread = True
    
    class Meta:
        db_backend = None
        db_addr = None

    def __new__(cls, *args, **kwargs):
        if hasattr(cls, 'db'):
            cls.initialized = cls.db.conn._is_open
        else:
            #log.debug("Configuring database at %s" % cls.Meta.db_addr)
            cls.db = cls.Meta.db_backend(cls.Meta.db_addr)
            cls.extent = cls.db.extent(cls.__name__)
        if not cls.initialized:
            #log.debug("Opening database connection...")
            cls.db.backend.open()
        if cls.multithread:
            schevo.mt.install(cls.db)
        assert cls.db.conn._is_open==True
        return super(Model, cls).__new__(cls)
    
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        
    def __str__(self):
        return str(self.Meta.db_addr)
    
    ### Public methods
    def save(self, commit=True):
        lock = self.db.write_lock()
        with lock:
            #if self.initialized:
            tx = self.extent.t.create(**self.kwargs)
            if commit:
                self.db.execute(tx)
                self.db._commit()
        lock.release()
        return self

    #def __getattr__(self, name):
    #    assert self.initialized==True
    #    return getattr(self.db, name)

class ModelManager(ModelBase):
    def __new__(cls, *args, **kwargs):
        cls.model = args[0]()
        cls.db = cls.model.db
        cls.extent = cls.model.extent
        cls.objects = RelationProxy(cls.extent)
        return super(ModelManager, cls).__new__(cls)
    def __call__(self, *args, **kwargs):
        self._default_manager = self.db
        return self
