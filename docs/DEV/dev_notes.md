# Developers' Notes

## Recalculation of Managed Attributes

The key to making the caching works as intended is to determine when the data descriptor should recalculate/recompute the private attribute through the getter.

Currently, recalculation is tracked via a instance attribute, named `_recalculate`, tagged to the data descriptor `lazyproperty`.

Check is implemented at the `__get__(self, instance, owner)` method of `lazyproperty` to check if the data descriptor should recalculate the value of the managed attribute through the `self._fget(...)` getter method.

## What's the Problem? What was it meant to solve?

Facts:

* The data descriptor can only know what is the updated value of the managed attribute by calculating through its getter method.
```python
@property # `property` equivalent to `lazyproperty(True)`
def name(self): # `name` is the getter
    return self._name # it is this return value `self._name` that allows the data descriptor to have 'access' to the updated value after it has been reset by the caller of the `setter(...)` method.
```

