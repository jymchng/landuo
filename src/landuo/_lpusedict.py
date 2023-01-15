from .lazyproperty import lazyproperty
from weakref import WeakSet
from .exceptions import *
from . import _states
import logging

logger = logging.getLogger(__name__)


class BaseMutableLazyProperty(lazyproperty, immutable=False):

    mutablelpinst = WeakSet()

    def __init_subclass__(
            cls,
            immutable: bool,
            use_instance_dict: bool,
            **init_subclass_kwargs):
        return super().__init_subclass__(immutable, use_instance_dict, **init_subclass_kwargs)

    def __new__(cls, fget, *, fset=_states._unimplemented, fdel=_states._unimplemented):
        obj = object.__new__(cls)
        cls.mutablelpinst.add(obj)
        logger.debug(f"***")
        logger.debug(f"In {cls.__name__=}'s *__new__, {cls=}, {obj=}")
        logger.debug(f"In {cls.__name__=}'s *__new__, {cls._prefix=}")
        logger.debug(f"In {cls.__name__=}'s *__new__, {cls._private_var_name=}")
        logger.debug(f"In {cls.__name__=}'s *__new__, {fget=}")
        logger.debug(f"In {cls.__name__=}'s *__new__, {fset=}")
        logger.debug(f"In {cls.__name__=}'s *__new__, {fdel=}")
        return obj

    def __init__(self, fget, *, fset=_states._unimplemented, fdel=_states._unimplemented): # doesn't know about self.name yet
        self._fget = fget
        logger.debug(f"In {self.__class__.__name__=}'s __init__, {self._fget=}")
        self._fset = fset
        logger.debug(f"In {self.__class__.__name__=}'s __init__, {self._fset=}")
        self._fdel = fdel
        logger.debug(f"In {self.__class__.__name__=}'s __init__, {self._fdel=}")

    def __set__(self, instance, value):
        if self._fset is _states._unimplemented:
            raise SetterUnimplemented(self.name, _states._unimplemented)
        self._fset(instance, value)
        for instance_of_subclasses in self.mutablelpinst:
            instance_of_subclasses._recalculate = True

    def setter(self, fset):
        logger.debug(f"In {self.__class__.__name__=}'s setter, {fset=}")
        mutablelazyprop = self.__class__(self._fget, fset=fset, fdel=self._fdel)
        mutablelazyprop.name = self.name
        logger.debug(f"In {self.__class__.__name__=}'s setter, {self=}")
        logger.debug(f"In {self.__class__.__name__=}'s setter, {mutablelazyprop.name=}")
        logger.debug(f"In {self.__class__.__name__=}'s setter, {mutablelazyprop._prefix=}")
        logger.debug(f"In {self.__class__.__name__=}'s setter, {mutablelazyprop._fget=}")
        logger.debug(f"In {self.__class__.__name__=}'s setter, {mutablelazyprop._fset=}")
        logger.debug(f"In {self.__class__.__name__=}'s setter, {mutablelazyprop._fdel=}")
        logger.debug(f"In {self.__class__.__name__=}'s setter, {mutablelazyprop=}")
        del self
        return mutablelazyprop

    def deleter(self, fdel):
        mutablelazyprop = type(self)(self._fget, fset=self._fset, fdel=fdel)
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
            **init_subclass_kwargs):
        return super().__init_subclass__(immutable, use_instance_dict, **init_subclass_kwargs)

    @staticmethod
    def func(instance):
        raise TypeError(
            "Cannot use cached_property instance without calling "
            "__set_name__() on it."
        )

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
