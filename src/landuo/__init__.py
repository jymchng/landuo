from .cachedproperty import cachedproperty
from . import (
    _lpnotusedict,
    _lpusedict,
    _states,
)

version = "0.2.1"


property = cachedproperty(immutable=False)
cached_property = cachedproperty(immutable=False)
