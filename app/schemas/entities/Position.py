class Position:
    def __init__(self, name):
        self._name = name

    # Getter
    @property
    def name(self):
        return self._name

    # ToString
    def __str__(self):
        return f"Position: {self._name}"