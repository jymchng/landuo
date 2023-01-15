from weakref import WeakKeyDictionary
from ._lpusedict import BaseMutableLazyProperty, BaseImmutableLazyProperty
from typing import Any
from . import _states
from .exceptions import *


class NotUseDictMutableLazyProperty(
        BaseMutableLazyProperty,
        immutable=False,
        use_instance_dict=False):

    _class_cache: WeakKeyDictionary

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self in self._class_cache and not self._recalculate:
            return self._class_cache[self]
        self._class_cache[self] = value = self._fget(instance)
        self._recalculate = False
        return value

    def __set__(self, instance, value):
        if self._fset is _states._unimplemented:
            raise SetterUnimplemented(self.name, _states._unimplemented)
        self._fset(instance, value)
        for instance_of_subclasses in self._class_cache.keys():
            instance_of_subclasses._recalculate = True


class NotUseDictImmutableLazyProperty(
        BaseImmutableLazyProperty,
        immutable=True,
        use_instance_dict=False):

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self in self._class_cache and not self._recalculate:
            return self._class_cache[self]
        self._class_cache[self] = value = self._fget(instance)
        self._recalculate = False
        return value
