from weakref import WeakKeyDictionary
from ._lpusedict import BaseMutableLazyProperty, BaseImmutableLazyProperty
from . import _states
from .exceptions import *
from typing import Union, Any, Type
from contextlib import redirect_stdout
import io
import logging
from ._states import _notavalue

logger = logging.getLogger(__name__)


class NotUseDictMutableLazyProperty(
        BaseMutableLazyProperty,
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
        self._recalculate = False

    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self in self._instance_cache and not self._recalculate:
            return self._instance_cache[instance]
        self._instance_cache[instance] = value = self._fget(instance)
        self._recalculate = False
        return value

    def __set__(self, instance, value):
        if self._fset is _states._unimplemented:
            raise SetterUnimplemented(self.name, _states._unimplemented)
        self._fset(instance, value)
        for instance_of_subclasses in self._class_cache.keys():
            instance_of_subclasses._recalculate = True

    def __delete__(self, instance):
        _delete_(self, instance)


class NotUseDictImmutableLazyProperty(
        NotUseDictMutableLazyProperty,
        immutable=True,
        use_instance_dict=False):

    def __set__(self, instance, value):
        raise AttributeError(
            f"The lazyproperty `{self.name}` is set to be immutable.")

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
