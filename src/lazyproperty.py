import logging
import sys
from weakref import WeakKeyDictionary
from typing import Any

logger = logging.getLogger(__name__)


class lazyproperty:
    _registry = dict()
    name = None
    _class_cache: WeakKeyDictionary['BaseMutableLazyProperty',
                                    Any] = WeakKeyDictionary()

    def __init_subclass__(
            cls,
            immutable: bool,
            use_instance_dict: bool = True,
            prefix: str = '',
            private_var_name: str = '',
            **init_subclass_kwargs):

        super().__init_subclass__(**init_subclass_kwargs)
        cls._prefix = prefix or ''
        cls._private_var_name = private_var_name or ''
        cls._registry[(immutable, use_instance_dict)] = cls
        logger.info(cls._registry)

    def __new__(cls, immutable, use_instance_dict=True):
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
        if self.name in instance.__dict__ and not self._recalculate:
            return instance.__dict__[self.name]
        # set it to attribute of the instance since instance.__dict__ will be
        # look up first
        instance.__dict__[self.name] = value = self._fget(instance)
        self._recalculate = False
        return value

    def _get_class_cache(self):
        return self._class_cache
