from .cachedproperty import cachedproperty
from . import (
    _lpnotusedict,
    _lpusedict,
    _states,
)

version = "1.0.0"


property = cachedproperty(immutable=False)
cached_property = cachedproperty(immutable=False)
