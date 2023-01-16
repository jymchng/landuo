# Getting Started

Read [Installation](installation.md) to install `landuo` first.

# For Existing Project

If you have an existing project which already uses the python's inbuilt `property`,

* add `landuo` to your dependencies,
* add the following declaration into the import declarations in your modules that use the python's inbuilt `property`.
```python
from landuo import property
#... other import statements
```

That's it! All your original `property` should now have be cached. By default, the cache used is the instance's attribute `__dict__`, read more at [APIs: cachedproperty](APIs/cachedproperty.md).


