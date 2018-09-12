"""不可改变字典相关
"""
def is_immutable(self):
    """不可改变的错误"""
    raise TypeError('%r 对象是不可改变的' % self.__class__.__name__)


class ImmutableDict(dict):
    """一个不可改变的字典"""
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
