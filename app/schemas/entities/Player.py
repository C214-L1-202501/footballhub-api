class Player:
    def __init__(self, name, age, position, country, number):
        self.__name = name
        self.__age = age
        self.__position = position
        self.__country = country
        self.__number = number

    # Getters
    @property
    def name(self):
        return self.__name

    @property
    def age(self):
        return self.__age

    @property
    def position(self):
        return self.__position

    @property
    def country(self):
        return self.__country

    @property
    def number(self):
        return self.__number

    def __str__(self):
        return f"Player: {self.__name}, Age: {self.__age}, Position: {self.__position}, Country: {self.__country}, Number: {self.__number}"
