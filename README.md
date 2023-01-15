# landuo (lazyproperty)
_just a property but lazier_...

Simply put, `lazyproperty` = `property` + `cached_property`.

Version: 0.2.0

# Reasons for Creating This
1. In-built [`property`](https://docs.python.org/3/library/functions.html#property) decorator allows you to manage your instances' attributes but at a cost of repeated computation for each read of the attribute.
2. `cached_property` built by many [1], allows you to cache your instances' attributes but at a cost of losing the ability to implement `setter` methods of them.

`lazyproperty` (used interchangably with `cached property` or its variants) solves this problem by caching of the values of your instances' attributes AND implementing `setter` methods for each of them.

# Objectives
|Objective|Description|Status|
|:--|:--|:--|
|Backward compatibility|It should be 'easy' (ideally, by adding a one-liner) to existing project to incorporate caching in property.|![](https://badgen.net/badge/status/completed/green)|
|Caching|Property must be cached. It should allow the use of another 'cache' beyond the instance's `__dict__` attribute for instances whose `__dict__` attribute is a non-mutable mapping. Read [more](https://docs.python.org/3/library/functools.html#cached_property).|Kinda?|
|Setter method is available|Cached property should allow for the implementation of `.setter(self, value)` method.|![](https://badgen.net/badge/status/completed/green)|
|Deleter method is available|Cached property should allow for the implementation of `.deleter(self)` method.|![](https://badgen.net/badge/status/completed/green)|
|Async compatibility|Cached property should be thread-safe. pydanny's [`cached_property`](https://github.com/pydanny/cached-property/blob/master/cached_property.py) allows for this.|No plans to do that in near future.
|Properties should be inherited as it is.|An example would be best here, if `self.name` returns `self._name` for a superclass, then for the subclass `self.name` should still return `self._name`, UNLESS wilfully overridden, e.g. `self.name` returns `f'Hi, I'm {super().name}`, the subclass' managed attribute `name` prepends `'Hi, I'm '`.|![](https://badgen.net/badge/status/completed/green)|



# How to Use
## For Existing Project

If you have an existing project which already uses the python's inbuilt `property`,

* add `landuo` to your dependencies,
* add the following declaration into the import declarations in your modules that use the python's inbuilt `property`.
```python
from landuo import property
#... other import statements
```

That's it! All your original `property` should now have be cached. By default, the cache used is the instance's attribute `__dict__`, read more at [APIs: lazyproperty](APIs/lazyproperty.md).

# Glossary

Managed Attribute(s) - The set of attribute(s) of a class which is managed by the `lazyproperty` / `property` object. To 'manage' means that the 'read' and/or 'write' capabilities of the attribute is decided by another python object.

Private Variable(s) - Python has no strictly 'private' variable. In this case, the 'private' variable refers to the attribute of a class that is managed by another python object.

Example:
```python
class Person:
    def __init__(self, name):
        self._name = name
        # self._name is referred as the 'private' variable

    @property # `property` manages `self.name` and its underlying private variable is `self._name`
    def name(self):
        return self._name
```

# References
[1] Here is a list of implementations for '`cached_property`'.

*    functools' [`cached_property`](https://docs.python.org/3/library/functools.html#cached_property)<br>
*    pydanny's [`cached_property`](https://github.com/pydanny/cached-property/blob/master/cached_property.py)<br>
*    penguinolog's [`cached_property`](https://github.com/penguinolog/backports.cached_property/blob/master/backports/cached_property/__init__.py) <br>
*    werkzeug's [`cached_property`](https://tedboy.github.io/flask/_modules/werkzeug/utils.html#cached_property) <br>
*    bottles' [`cached_property`](https://github.com/bottlepy/bottle/blob/df67999584a0e51ec5b691146c7fa4f3c87f5aac/bottle.py#L215)<br>
*    bottles' [`lazy_attribute`](https://github.com/bottlepy/bottle/blob/df67999584a0e51ec5b691146c7fa4f3c87f5aac/bottle.py#L230)<br>
*    sad2project's [`LazyProperty`](https://github.com/sad2project/descriptor-tools/blob/master/src/descriptor_tools/properties.py#L10)<br>

# Why the Name `landuo`?

懒惰 (Hàn yǔ Pīn yīn: lănduò) means lazy in Chinese, which describes the `lazyproperty` class of this package.





