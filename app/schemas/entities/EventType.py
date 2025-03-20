class EventType:
    def __init__(self, name):
        self.__name = name

    # Getter
    @property
    def name(self):
        return self.__name

    # ToString
    def __str__(self):
        return f"EventType: {self.__name}"