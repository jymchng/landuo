from .lazyproperty import lazyproperty
from .exceptions import *
from . import _states
import logging
from contextlib import redirect_stdout
import io

logger = logging.getLogger(__name__)


class BaseMutableLazyProperty(lazyproperty, immutable=False):

    def __init_subclass__(
            cls,
            immutable: bool,
            use_instance_dict: bool,
            **init_subclass_kwargs):
        return super().__init_subclass__(
            immutable, use_instance_dict, **init_subclass_kwargs)

    def __new__(
            cls,
            fget,
            *,
            fset=_states._unimplemented,
            fdel=_states._unimplemented):
        obj = object.__new__(cls)
        return obj

    # doesn't know about self.name yet
    def __init__(
            self,
            fget,
            *,
            fset=_states._unimplemented,
            fdel=_states._unimplemented):
        self._fget = fget
        self._fset = fset
        self._fdel = fdel
        self._recalculate = False

    def __set__(self, instance, value):
        if self._fset is _states._unimplemented:
            raise SetterUnimplemented(self.name, _states._unimplemented)
        self._fset(instance, value)
        with redirect_stdout(io.StringIO()):
            instance.__dict__[self.name] = value = self._fget(instance)

    def setter(self, fset):
        mutablelazyprop = self.__class__(
            self._fget, fset=fset, fdel=self._fdel)
        mutablelazyprop.name = self.name
        del self
        return mutablelazyprop

    def deleter(self, fdel):
        mutablelazyprop = type(self)(self._fget, fset=self._fset, fdel=fdel)
        mutablelazyprop.name = self.name
        return mutablelazyprop


class BaseImmutableLazyProperty(lazyproperty, immutable=True):

    def __init_subclass__(
            cls,
            immutable: bool,
            use_instance_dict: bool,
            **init_subclass_kwargs):
        return super().__init_subclass__(
            immutable, use_instance_dict, **init_subclass_kwargs)

    def __new__(cls, fget, *, fdel=_states._unimplemented):
        obj = object.__new__(cls)
        return obj

    def __init__(self, fget, *, fdel=_states._unimplemented):
        self._fget = fget
        self._fdel = fdel
        self._recalculate = False

    def __set__(self, instance, value):
        raise AttributeError(
            f"The lazyproperty `{self.name}` is set to be immutable.")

    def deleter(self, fdel):
        mutablelazyprop = type(self)(self._fget, fdel=fdel)
        mutablelazyprop.name = self.name
        return mutablelazyprop
