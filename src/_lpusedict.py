from .lazyproperty import lazyproperty
from weakref import WeakSet
from .exceptions import *
from . import _states


class BaseMutableLazyProperty(lazyproperty, immutable=False):

    mutablelpinst = WeakSet()

    def __init_subclass__(
            cls,
            immutable: bool,
            use_instance_dict: bool,
            prefix: str = '',
            private_var_name: str = '',
            **init_subclass_kwargs):
        return super().__init_subclass__(immutable, use_instance_dict,
                                         prefix, private_var_name, **init_subclass_kwargs)

    def __new__(cls, fget, fset=None, fdel=None):
        obj = object.__new__(cls)
        cls.mutablelpinst.add(obj)
        return obj

    def __init__(self, fget, fset=None, fdel=None):
        self._fget = fget
        self._fset = _states._unimplemented
        self._fdel = _states._unimplemented
        self._recalculate = True

    def __set__(self, instance, value):
        if self._fset is _states._unimplemented:
            raise SetterUnimplemented(self.name, _states._unimplemented)
        self._fset(instance, value)
        for instance_of_subclasses in self.mutablelpinst:
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

    def __init_subclass__(
            cls,
            immutable: bool,
            use_instance_dict: bool,
            prefix: str = '',
            private_var_name: str = '',
            **init_subclass_kwargs):
        return super().__init_subclass__(immutable, use_instance_dict,
                                         prefix, private_var_name, **init_subclass_kwargs)

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
