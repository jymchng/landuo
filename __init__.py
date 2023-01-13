from landuo import (
    lazyproperty,
    _internals,
    _lpnotusedict,
    _lpusedict,   
)

property = lazyproperty.lazyproperty(immutable=False)