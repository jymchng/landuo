import logging
import sys
from weakref import WeakKeyDictionary
from typing import Union, Any
from ._internals import _missing, _notavalue

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    stream=sys.stdout)


class lazyproperty:
    _registry = dict()
    name = None
    _class_cache: WeakKeyDictionary['BaseMutableLazyProperty', Any] = WeakKeyDictionary()
    
    def __init_subclass__(
            cls,
            immutable: bool,
            use_instance_dict=False,
            prefix: str = '',
            private_var_name: str = '',
            **init_subclass_kwargs):
        super().__init_subclass__(**init_subclass_kwargs)
        cls._prefix = prefix or ''
        cls._private_var_name = private_var_name or ''
        cls._registry[(immutable, use_instance_dict)] = cls

    def __new__(cls, immutable, use_instance_dict=False):
        return cls._registry[(immutable, use_instance_dict)]

    def __set_name__(self, owner, name):
        preferred_name = self._private_var_name or (
            self._prefix +
            name) or (
            getattr(
                owner,
                'private_var_prefix',
                '') +
            name)
        self.name = preferred_name
        if name != self.name:
            raise TypeError(
                "Cannot assign the same cached_property to two different names "
                "(%r and %r)." %
                (self.name, name))
        logger.info(f"lazyproperty `{self.name}` has been initialized.")

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
        if instance is None:
            return self
        # if self._fget is None:
        #     raise Exception(f"lazyproperty `{self.name}` has been deleted.")
        if self in self._class_cache and not self._recalculate:
            return self._class_cache[self]
        # set it to attribute of the instance since instance.__dict__ will be
        # look up first
        self._class_cache[self] = value = self._fget(instance)
        self._recalculate = False
        return value
    
    def _get_class_cache(self):
        return self._class_cache


class BaseMutableLazyProperty(lazyproperty, immutable=False):
    
    def __new__(cls, fget, fset=None, fdel=None):
        obj = object.__new__(cls)
        cls._class_cache.update({obj: _notavalue})
        return obj

    def __init__(self, fget, fset=None, fdel=None):
        self._fget = fget
        self._fset = fset
        self._fdel = fdel
        self._recalculate = True

    def __set__(self, instance, value):
        if self._fset is None:
            raise Exception(f"lazyproperty `{self.name}` `setter` method is not implemented.")
        self._fset(instance, value)
        for instance_of_subclasses in self._class_cache.keys():
            instance_of_subclasses._recalculate = True                

    def setter(self, fset):
        mutablelazyprop = type(self)(self._fget, fset, self._fdel)
        mutablelazyprop.name = self.name
        del self
        return mutablelazyprop

    def deleter(self, fdel):
        mutablelazyprop = type(self)(self._fget, self._fset, fdel)
        mutablelazyprop.name = self.name
        return mutablelazyprop

    # def __delete__(self, instance):
    #     super().__delete__(instance)
    #     self._fset = None


class BaseImmutableLazyProperty(lazyproperty, immutable=True):

    @staticmethod
    def func(instance):
        raise TypeError(
            "Cannot use cached_property instance without calling "
            "__set_name__() on it."
        )

    def __new__(cls, fget, *, fset=None, fdel=None):
        obj = object.__new__(cls)
        return obj

    def __init__(self, fget, *, fdel=None):
        self._fget = fget
        self._fdel = fdel
        self._recalculate = False

    def __set__(self, instance, value):
        raise AttributeError(
            f"The lazyproperty `{self.name}` is set to be immutable.")

    def deleter(self, fdel):
        mutablelazyprop = type(self)(self._fget, fdel)
        mutablelazyprop.name = self.name
        return mutablelazyprop

property = lazyproperty(immutable=False, use_instance_dict=False)
