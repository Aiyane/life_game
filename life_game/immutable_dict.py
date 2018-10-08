"""Dictionary that cannot be chaneged.
"""
def is_immutable(self):
    """when dict modify will raise error"""
    raise TypeError('%r object is cannot be changed.' % self.__class__.__name__)


class ImmutableDict(dict):
    """a dict that cannot be changed"""
    _hash_cache = None

    def __reduce_ex__(self, protocol):
        return type(self), (dict(self),)

    def popitem(self):
        is_immutable(self)

    def __setitem__(self, key, value):
        is_immutable(self)

    def __delitem__(self, key):
        is_immutable(self)

    def clear(self):
        is_immutable(self)

    def __repr__(self):
        return '%s(%s)' % (
            self.__class__.__name__,
            dict.__repr__(self),
        )

    def copy(self):
        return dict(self)

    def __copy__(self):
        return self
