from . import (
    _lpnotusedict,
    _lpusedict,
    _states,
)

from .lazyproperty import lazyproperty

property = lazyproperty(immutable=False)
cached_property = lazyproperty(immutable=False)
