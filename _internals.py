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
    
class _set_with_at_most_one_element:
    
    def __init__(self, stmt=None):
        self.set = set()
        if stmt is not None:
            self.set.add(stmt)

    def add(self, element):
        if len(self.set) >= 1:
            raise ValueError("Cannot add more than one element to this set.")
        self.set.add(element)

    def remove(self, element):
        self.set.remove(element)

    def get_element(self):
        if len(self.set) == 0:
            return None
        else:
            return self.set.pop()
            
    def __contains__(self, element):
        return element in self.set

_missing = _Missing()
_notavalue = _NotAValue()