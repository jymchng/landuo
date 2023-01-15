from weakref import WeakKeyDictionary
from ._lpusedict import BaseMutableLazyProperty, BaseImmutableLazyProperty
from . import _states
from .exceptions import *
from typing import Union, Any, Type
from contextlib import redirect_stdout
import io
import logging

logger = logging.getLogger(__name__)


class NotUseDictMutableLazyProperty(
        BaseMutableLazyProperty,
        immutable=False,
        use_instance_dict=False):

    _class_cache: WeakKeyDictionary

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self in self._class_cache:
            return self._class_cache[self]
        self._class_cache[self] = value = self._fget(instance)
        return value

    def __set__(self, instance: Any, value: Any):
        if self._fset is _states._unimplemented:
            raise SetterUnimplemented(self.name, _states._unimplemented)
        self._fset(instance, value)
        with redirect_stdout(io.StringIO()):
            self._class_cache[self] = value = self._fget(instance)

    def __delete__(self, instance):
        _delete_(self, instance)


class NotUseDictImmutableLazyProperty(
        BaseImmutableLazyProperty,
        immutable=True,
        use_instance_dict=False):

    def __get__(self, instance: Any, owner: Type[Any]):
        if instance is None:
            return self
        if self in self._class_cache:
            return self._class_cache[self]
        self._class_cache[self] = value = self._fget(instance)
        return value

    def __delete__(self, instance):
        _delete_(self, instance)


def _delete_(descriptor_obj: Union[NotUseDictImmutableLazyProperty,
             NotUseDictMutableLazyProperty], instance: Any):
    if descriptor_obj._fdel is _states._unimplemented:
        raise AttributeError(
            f"lazyproperty '{descriptor_obj.name}' has no deleter.")
    if descriptor_obj in descriptor_obj._class_cache:
        del descriptor_obj._class_cache[descriptor_obj]
    descriptor_obj._fdel(instance)
    del descriptor_obj
