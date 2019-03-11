class Object(object):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self._ident = None
        self.update(kwargs)
        del kwargs
        self.update(locals())
        del self.self

    @property
    def ident(self):
        return self._ident

    @ident.setter
    def ident(self, value):
        self._ident = value

    def update(self, data: dict):
        for key, value in data.items():
            setattr(self, key, value)
