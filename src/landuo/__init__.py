from . import (
    _lpnotusedict,
    _lpusedict,
    _states,
)

version = "0.2.0"

from .lazyproperty import lazyproperty

property = lazyproperty(immutable=False)
cached_property = lazyproperty(immutable=False)
