# Developers' Notes

## Recalculation of Managed Attributes

The key to making the caching works as intended is to determine when the data descriptor should recalculate/recompute the private attribute through the getter.

Currently, recalculation is tracked via a instance attribute, named `_recalculate`, tagged to the data descriptor `lazyproperty`.

Check is implemented at the `__get__(self, instance, owner)` method of `lazyproperty` to check if the data descriptor should recalculate the value of the managed attribute through the `self._fget(...)` getter method.

## What's the Problem? What was it meant to solve?

Facts:

* The data descriptor can only know what is the updated value (after `setter(...)` method is called) of the managed attribute by calculating through (calling) its getter method.
```python
@property # `property` equivalent to `lazyproperty(True)`
def name(self): # `name` is the getter
    return self._name # it is this return value `self._name` that allows the data descriptor to have 'access' to the updated value after it has been reset by the caller of the `setter(...)` method.
```
```python
# in data descriptor's __get__
# PSEUDOCODE
if not self._recalculate and value_in_cache:
    ...retrieve from cache...
else:
    ... call getter(...) and cache returned value... 
```
* This is because the idiom of the `setter(...)` method assigns the 'new' value of the managed attribute to the 'private' variable **WITHOUT returning it**.
```python
# continuing previous example of `name`
@name.setter
def name(self, value):
    self._name = value
    # no return value
```
