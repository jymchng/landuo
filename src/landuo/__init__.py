from . import (
    _lpnotusedict,
    _lpusedict,
    _states,
)

version = "0.2.1"

from .lazyproperty import lazyproperty

property = lazyproperty(immutable=False)
cached_property = lazyproperty(immutable=False)
