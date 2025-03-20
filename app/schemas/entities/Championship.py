class Championship:
    def __init__(self, name, country, type, season):
        self.__name = name
        self.__country = country
        self.__type = type
        self.__season = season

    # Getter
    @property
    def name(self):
        return self.__name
    
    @property
    def country(self):
        return self.__country

    @property
    def type(self):
        return self.__type
    
    @property
    def season(self):
        return self.__season

    # ToString
    def __str__(self):
        return f"Championship(name={self.__name}, country={self.__country}, type={self.__type}, season={self.__season})"
