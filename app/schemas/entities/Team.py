class Team:
    def __init__(self, name, nickname, city, country, founding_date):
        self.__name = name
        self.__nickname = nickname
        self.__city = city
        self.__country = country
        self.__founding_date = founding_date

    # Getters
    @property
    def name(self):
        return self.__name

    @property
    def nickname(self):
        return self.__nickname

    @property
    def city(self):
        return self.__city

    @property
    def country(self):
        return self.__country

    @property
    def founding_date(self):
        return self.__founding_date

    # ToString
    def __str__(self):
        return f"Team: {self.__name}, Nickname: {self.__nickname}, City: {self.__city}, Country: {self.__country}, Founding Date: {self.__founding_date}"