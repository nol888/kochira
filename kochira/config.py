def _id(x):
    return x


class Field:
    _sentinel = object()
    _total_creation_order = 0

    def __init__(self, type=_id, doc="(undocumented)", default=_sentinel):
        self.type = type
        self.doc = doc
        self.default = default
        self._creation_order = self._total_creation_order
        self.__class__._total_creation_order += 1

    def unpack(self, value):
        return self.type(value)

    def __get__(self, obj, type=None):
        if obj is None:
            return self

        v = obj._fields.get(self.name, self.default)

        if v is Field._sentinel:
            if hasattr(self.type, "get_default"):
                return self.type.get_default()

            raise AttributeError(self.name)

        return v

    def __set__(self, obj, v):
        obj._fields[self.name] = v


class _ConfigMeta(type):
    def __new__(cls, name, bases, dct):
        newcls = type.__new__(cls, name, bases, dct)

        newcls._field_mappings = {}

        for base in bases:
            if hasattr(base, "_field_mappings"):
                newcls._field_mappings.update(base._field_mappings)

        for k, f in dct.items():
            if not isinstance(f, Field):
                continue
            f.name = k
            newcls._field_mappings[k] = f

        newcls._field_defs = sorted(newcls._field_mappings.values(),
                                    key=lambda f: f._creation_order)

        return newcls


class Config(metaclass=_ConfigMeta):
    def __init__(self, values=None):
        if values is None:
            values = {}

        self._fields = {}

        for k, v in values.items():
            if k in self._field_mappings:
                v = self._field_mappings[k].unpack(v)

            self._fields[k] = v

    def __repr__(self):
        return "{}({})".format(
            self.__class__.__name__,
            ", ".join("{}={!r}".format(k, v) for k, v in self._fields.items())
        )

    @staticmethod
    def _resolve(mine, other):
        if isinstance(mine, Config):
            # if the other side is a config, then we'll just combine
            return mine.combine(other)
        elif isinstance(mine, dict):
            # if they're a dict, then we compose other into mine
            d = mine.copy()
            d.update(other)
            return d
        else:
            return other

    def combine(self, other):
        """
        Combine two configurations together. The other configuration must be
        a narrower (i.e. superclass or same) type as this one. The resulting
        configuration will be the wider (i.e. this) type.
        """

        if not issubclass(self.__class__, other.__class__):
            raise TypeError("other class is not this class or narrower")

        fields = self._fields.copy()

        # combine their fields
        for k, v in other._fields.items():
            if k in fields:
                # we need to perform conflict resolution
                fields[k] = Config._resolve(fields[k], v)
            else:
                fields[k] = v

        return self.__class__(fields)

    @classmethod
    def interior_type(cls):
        return cls


class Mapping:
    def __init__(self, type):
        self.type = type

    def __call__(self, m):
        return {k: self.type(v) for k, v in m.items()}

    def interior_type(self):
        if hasattr(self.type, "interior_type"):
            return self.type.interior_type()

        return self.type

    def get_default(self):
        return {}


class Many:
    def __init__(self, type):
        self.type = type

    def __call__(self, xs):
        return [self.type(x) for x in xs]

    def interior_type(self):
        if hasattr(self.type, "interior_type"):
            return self.type.interior_type()

        return self.type

    def get_default(self):
        return []
