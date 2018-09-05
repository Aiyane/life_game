class ConfigAttribute(object):
    """Makes an attribute forward to the config"""

    def __init__(self, name):
        self.__name__ = name

    def __get__(self, obj, type=None):
        if obj is None:
            return self
        return obj.config[self.__name__]

    def __set__(self, obj, value):
        obj.config[self.__name__] = value


class Config(dict):
    def __init__(self, defaults=None):
        dict.__init__(self, defaults or {})

    def from_object(self, obj):
        """例如:
        from yourapplication import default_config
        view.config.from_object(default_config)
        """
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, dict.__repr__(self))
