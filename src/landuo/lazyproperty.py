import logging
import sys
from weakref import WeakKeyDictionary
from typing import Any
import inspect

logger = logging.getLogger(__name__)


class lazyproperty:
    """Caches a managed property of a class.

    Arguments:
        immutable (bool): If `True`, managed property of a class cannot be set to other values.
        use_instance_dict (bool, optional): Defaults to `True`. If `True`, `lazyproperty` uses the instance's `__dict__` attribute as 
            the cache for the managed property. If `False`, `lazyproperty` uses a `weakref.WeakKeyDictionary` as the cache.
        prefix (str, optional): Defaults to '' - empty string. Tells `lazyproperty` the name of the 'private' attribute of the managed property.
        private_var_name (str, optional): Defaults to '' - empty string. Tells `lazyproperty` the exact name of the 'private' attribute stored 
            in the instance's `__dict__`.
            
    Examples:
        (1):
            from landuo import property # functions in the same way as inbuilt `@property` decorator.
        
            class Person:
                def __init__(self, name):
                    self._name = name
                
                @property # note that this `property` is `lazyproperty(True)`
                def name(self):
                    return self._name
            
                @name.setter
                def name(self, new_name):
                    self._name = new_name
            
            >>> henry = Person('Henry')
            >>> henry.name
            'Henry'
            >>> henry.name = 'James'
            >>> henry.name
            'James'
    """
    _registry = dict()
    name = None
    _class_cache: WeakKeyDictionary['BaseMutableLazyProperty',
                                    Any] = WeakKeyDictionary()

    def __init_subclass__(
            cls,
            immutable: bool,
            use_instance_dict: bool = True,
            **init_subclass_kwargs):

        super().__init_subclass__(**init_subclass_kwargs)
        
        cls._registry[(immutable, use_instance_dict)] = cls

    def __new__(cls, 
                immutable, 
                use_instance_dict=True,
                prefix: str = '',
                private_var_name: str = '',):
        
        cls._prefix = prefix or ''
        cls._private_var_name = private_var_name or ''
        return cls._registry[(immutable, use_instance_dict)]

    def __set_name__(self, owner, name):
        owner_set_private_var_prefix = getattr(
                owner,
                'private_var_prefix',
                '')
        any_prefix = self._prefix or owner_set_private_var_prefix
        self.private_var_name = self._private_var_name or (any_prefix + name)
        self.name = name
        if name != self.name:
            raise TypeError(
                "Cannot assign the same cached_property to two different names "
                "(%r and %r)." %
                (self.name, name))
        logger.info(f"lazyproperty {self=} with name: `{self.name}` has been initialized.")

    # logger.debug(f"{self.__class__.__name__=}'s __set_name__ is called with owner = {owner}, name = {name}, {self.name=}!")
    # def __delete__(self, instance):
    #     print(f"In {self.__class__.__name__}'s __delete__, {self=}, {instance=}")
    #     if self._fdel is None:
    #         raise AttributeError(f"lazyproperty '{self.name}' has no deleter")
    #     if self.name in instance.__dict__:
    #         del instance.__dict__[self.name]
    #         # del obj.__dict__[self.name]
    #     self._fdel(instance)
    #     self._fget = None
    #     del self

    def __get__(self, instance, owner):
        self.cached_name = self.private_var_name or self.name
        if instance is None:
            return self
        if self.cached_name in instance.__dict__ and not self._recalculate:
            return instance.__dict__[self.cached_name]
        instance.__dict__[self.cached_name] = value = self._fget(instance)
        self._recalculate = False
        return value

    def _get_class_cache(self):
        return self._class_cache

    def _get_registry(self):
        return self._registry
