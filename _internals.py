class _Missing(object):

    def __repr__(self):
        return 'MISSING'

    def __reduce__(self):
        return '_MISSING'

class _NotAValue(object):

    def __repr__(self):
        return 'NOTAVALUE'

    def __reduce__(self):
        return '_NOTAVALUE'

_missing = _Missing()
_notavalue = _NotAValue()