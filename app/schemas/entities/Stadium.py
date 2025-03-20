class Stadium:
    def __init__(self, name, city, country):
        self.__name = name
        self.__city = city
        self.__country = country

    # Getters
    @property
    def name(self):
        return self.__name

    @property
    def city(self):
        return self.__city

    @property
    def country(self):
        return self.__country

    # ToString
    def __str__(self):
        return f"Stadium: {self.__name}, City: {self.__city}, Country: {self.__country}"