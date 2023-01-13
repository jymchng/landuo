from ._lpusedict import BaseMutableLazyProperty, BaseImmutableLazyProperty
from typing import Any

class NotUseDictMutableLazyProperty(BaseMutableLazyProperty, immutable=False, use_instance_dict=False):
    
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
    
    def __set__(self, instance, value):
        if self._fset is None:
            raise Exception(f"lazyproperty `{self.name}` `setter` method is not implemented.")
        self._fset(instance, value)
        for instance_of_subclasses in self._class_cache.keys():
            instance_of_subclasses._recalculate = True
        
class NotUseDictImmutableLazyProperty(BaseImmutableLazyProperty, immutable=True, use_instance_dict=False):
    
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