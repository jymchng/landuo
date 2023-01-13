import logging
import sys

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                        stream=sys.stdout)

class lazyproperty:
    _registry = dict()
    subclasses_inst_list = list()
    name = None
    
    def __init_subclass__(cls, immutable: bool, prefix: str='', private_var_name: str='', **init_subclass_kwargs):
        super().__init_subclass__(**init_subclass_kwargs)
        cls._prefix = prefix
        cls._private_var_name = private_var_name
        cls._registry[immutable] = cls
        
    def __new__(cls, immutable):
        return cls._registry[immutable]
    
    def __set_name__(self, owner, name):
        preferred_name = self._private_var_name or (self._prefix + name) or (getattr(owner, 'private_var_prefix', '') + name)
        self.name = preferred_name
        if name != self.name:
            raise TypeError(
                "Cannot assign the same cached_property to two different names "
                "(%r and %r)." % (self.name, name)
            )
        logger.info(f"lazyproperty `{self.name}` has been initialized.")
        
    # logger.debug(f"{self.__class__.__name__=}'s __set_name__ is called with owner = {owner}, name = {name}, {self.name=}!")     
    # def __delete__(self, instance):
    #     print(f"In {self.__class__.__name__}'s __delete__, {self=}, {instance=}")
    #     if self.fdel is None:
    #         raise AttributeError(f"lazyproperty '{self.name}' has no deleter")
    #     if self.name in instance.__dict__:
    #         del instance.__dict__[self.name]
    #         # del obj.__dict__[self.name]
    #     self.fdel(instance)
    #     self.fget = None
    #     del self
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        if self.fget is None:
            raise Exception(f"lazyproperty `{self.name}` has been deleted.")
        if self.name in instance.__dict__ and not self.recalculate:
            return instance.__dict__[self.name]     
        instance.__dict__[self.name] = value = self.fget(instance) # set it to attribute of the instance since instance.__dict__ will be look up first
        self.recalculate = False
        return value
    
class BaseMutableLazyProperty(lazyproperty, immutable=False):
        
    def __new__(cls, fget, fset=None, fdel=None):
        obj = object.__new__(cls)
        cls.subclasses_inst_list.append(obj)
        return obj
        
    def __init__(self, fget, fset=None, fdel=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.recalculate = False
    
    def __set__(self, instance, value):
        if self.fset is None:
            raise Exception(f"lazyproperty `{self.name}` has been deleted.")
        self.fset(instance, value)
        for instance_of_subclasses in self.subclasses_inst_list:
            boolvar = instance_of_subclasses.recalculate
            if not boolvar:
                instance_of_subclasses.recalculate = True
        
    def setter(self, fset):
        mutablelazyprop = type(self)(self.fget, fset, self.fdel)
        mutablelazyprop.name = self.name
        del self
        return mutablelazyprop
    
    def deleter(self, fdel):
        mutablelazyprop = type(self)(self.fget, self.fset, fdel)
        mutablelazyprop.name = self.name
        return mutablelazyprop
    
    # def __delete__(self, instance):
    #     super().__delete__(instance)
    #     self.fset = None
        
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
        self.fget = fget
        self.fdel = fdel
        self.recalculate = False        
       
    def __set__(self, instance, value):
        raise AttributeError(f"The lazyproperty `{self.name}` is set to be immutable.")

    def deleter(self, fdel):
        mutablelazyprop = type(self)(self.fget, fdel)
        mutablelazyprop.name = self.name
        return mutablelazyprop
    
property = lazyproperty(immutable=False)