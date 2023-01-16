import logging
from typing import Type
from . import _states

logger = logging.getLogger(__name__)


class cachedproperty:
    """Caches a managed property of a class.

    Arguments:
        immutable (bool): If `True`, managed property of a class cannot be set to other values.
        use_instance_dict (bool, optional): If `True`, `cachedproperty` uses the instance's `__dict__` attribute as the cache for the managed property. If `False`, `cachedproperty` uses a `weakref.WeakKeyDictionary` as the cache.
            Defaults to `True`.
        prefix (str, optional): Tells `cachedproperty` the prefix of the 'private' attribute of the managed property. e.g. If the managed property of the class is `name` and the 'private' attribute of it is `_name`, then the prefix is `'_'`.
            Defaults to `""`.
        private_var_name (str, optional): Tells `cachedproperty` the exact name of the 'private' attribute stored in the instance's `__dict__`. e.g. If the managed property of the class is `name` and the 'private' attribute of it is `_name`, then the private_var_name is `'_name'`.
            Defaults to `""`.

    Examples:

        (1)

            from landuo import property # functions in the same way as inbuilt `@property` decorator.

            class Person:
                def __init__(self, name):
                    self._name = name

                @property # note that this `property` is `cachedproperty(True)`
                def name(self):
                    return self._name

                @name.setter
                def name(self, new_name):
                    self._name = new_name

            >>> henry = Person('Henry')
            >>> henry.name
            'Henry'
            >>> henry.name = 'James'
            >>> henry.name
            'James'
        (2)

            from landuo import cachedproperty

            class Person:
                def __init__(self, name):
                    self._name = name

                @cachedproperty(immutable=False, use_instance_dict=True) # returns a managed attribute whose cache is the
                # instance of Person's `__dict__` attribute
                def name(self):
                    return self._name

                @name.setter # if the managed attribute `name`'s `immutable` parameter into the `cachedproperty` decorator is set
                # to `False`, then this will raise an AttributeError as the managed attribute `name` has no `setter` method.
                def name(self, new_name):
                    self._name = new_name
    """
    _registry: dict[(bool, bool), Type] = dict()
    name: str = None

    def __init_subclass__(
            cls,
            immutable: bool,
            use_instance_dict: bool = True,
            **init_subclass_kwargs):

        super().__init_subclass__(**init_subclass_kwargs)

        cls._registry[(immutable, use_instance_dict)] = cls

    def __new__(cls,
                immutable: bool,
                use_instance_dict=True,
                prefix: str = '',
                private_var_name: str = '',):

        cls._prefix = prefix or ''
        cls._private_var_name = private_var_name or ''
        return cls._registry[(immutable, use_instance_dict)]

    def __set_name__(self, owner, name):
        owner_set_private_var_prefix: str = getattr(
            owner,
            'private_var_prefix',
            '')
        any_prefix: str = self._prefix or owner_set_private_var_prefix
        self.private_var_name = self._private_var_name or (any_prefix + name)
        self.name = name

        if name != self.name:
            raise TypeError(
                "Cannot assign the same cachedproperty to two different names "
                "(%r and %r)." %
                (self.name, name))
        logger.info(
            f"cachedproperty {self=} with name: `{self.name}` has been initialized.")

    def __delete__(self, instance):
        if self._fdel is _states._unimplemented:
            raise AttributeError(
                f"cachedproperty '{self.name}' has no deleter.")
        if self.name in instance.__dict__:
            del instance.__dict__[self.name]
        self._fdel(instance)
        del self

    def __get__(self, instance, owner):
        self.cached_name = self.private_var_name or self.name
        if instance is None:
            return self
        if self.cached_name in instance.__dict__:
            return instance.__dict__[self.cached_name]
        instance.__dict__[self.cached_name] = value = self._fget(instance)
        return value

    def _get_registry(self):
        return self._registry
