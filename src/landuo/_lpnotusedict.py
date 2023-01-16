from weakref import WeakKeyDictionary
from ._lpusedict import BaseImmutableCachedProperty, BaseMutableCachedProperty
from . import _states
from .exceptions import *
from typing import Union, Any, Type
from contextlib import redirect_stdout
import io
import logging
from ._states import _notavalue

logger = logging.getLogger(__name__)


class NotUseDictMutableCachedProperty(
        BaseMutableCachedProperty,
        immutable=False,
        use_instance_dict=False):

    def __init__(
            self,
            fget,
            *,
            fset=_states._unimplemented,
            fdel=_states._unimplemented):
        super().__init__(fget, fset=fset, fdel=fdel)
        self._instance_cache = WeakKeyDictionary()

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if instance in self._instance_cache:
            return self._instance_cache[instance]
        self._instance_cache[instance] = value = self._fget(instance)
        return value

    def __set__(self, instance, value):
        if self._fset is _states._unimplemented:
            raise SetterUnimplemented(self.name, _states._unimplemented)
        self._fset(instance, value)
        with redirect_stdout(io.StringIO()):
            self._instance_cache[instance] = value = self._fget(instance)

    def __delete__(self, instance):
        _delete_(self, instance)


class NotUseDictImmutableCachedProperty(
        NotUseDictMutableCachedProperty,
        immutable=True,
        use_instance_dict=False):

    def __set__(self, instance, value):
        raise AttributeError(
            f"The cachedproperty `{self.name}` is set to be immutable.")


def _delete_(descriptor_obj: Union[NotUseDictMutableCachedProperty,
             NotUseDictImmutableCachedProperty], instance: Any):
    if descriptor_obj._fdel is _states._unimplemented:
        raise AttributeError(
            f"cachedproperty '{descriptor_obj.name}' has no deleter.")
    if descriptor_obj in descriptor_obj._class_cache:
        del descriptor_obj._class_cache[descriptor_obj]
    descriptor_obj._fdel(instance)
    del descriptor_obj
