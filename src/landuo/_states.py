class _Missing(object):

    def __repr__(self):
        return 'MISSING'

    def __reduce__(self):
        return '_MISSING'

    def __str__(self):
        return "missing"


class _NotAValue(object):

    def __repr__(self):
        return 'NOTAVALUE'

    def __reduce__(self):
        return '_NOTAVALUE'

    def __str__(self):
        return "not a value"


class _Unimplemented(object):

    def __repr__(self):
        return 'UNIMPLEMENTED'

    def __reduce__(self):
        return '_UNIMPLEMENTED'

    def __str__(self):
        return "unimplemented"


class _Deleted(object):

    def __repr__(self):
        return 'DELETED'

    def __reduce__(self):
        return '_DELETED'

    def __str__(self):
        return "deleted"


_missing = _Missing()
_notavalue = _NotAValue()
_unimplemented = _Unimplemented()
_deleted = _Deleted()
