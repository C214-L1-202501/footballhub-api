class Country:
    def __init__(self, name: str):
        self.__name = name

    @property
    def name(self):
        return self.__name

    def __repr__(self):
        return f"Country(name='{self.__name}')"
