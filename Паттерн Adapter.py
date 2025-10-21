from abc import ABC, abstractmethod


# Интерфейс Транспорт
class Transport(ABC):
    @abstractmethod
    def drive(self, road):
        pass


# Интерфейс Дорога
class Road(ABC):
    @abstractmethod
    def get_road_type(self):
        pass


# Конкретная реализация Дороги
class ConcreteRoad(Road):
    def __init__(self, road_type):
        self._road_type = road_type

    def get_road_type(self):
        return self._road_type


# Конкретный Транспорт - Машина
class Car(Transport):
    def drive(self, road):
        return f"Машина едет по {road.get_road_type()}"


# Объект, который НЕ является Транспортом
class Donkey:
    def eat(self):
        return "Осёл кушает сено"

    def walk(self):
        return "Осёл идёт медленно"


# Адаптер, который превращает Осла в Транспорт
class Saddle(Transport):
    def __init__(self, donkey):
        self._donkey = donkey

    def drive(self, road):
        # Адаптируем интерфейс Осла к интерфейсу Транспорта
        return f"Осёл с седлом движется по {road.get_road_type()} ({self._donkey.walk()})"


# Демонстрация работы
if __name__ == "__main__":
    # Создаем дороги
    highway = ConcreteRoad("шоссе")
    country_road = ConcreteRoad("проселочной дороге")

    # Обычный транспорт - машина
    car = Car()
    print(car.drive(highway))

    # Осёл без адаптера
    donkey = Donkey()
    print(donkey.eat())
    # print(donkey.drive(highway))  # Это вызвало бы ошибку

    # Осёл с адаптером (седлом) становится транспортом
    donkey_with_saddle = Saddle(donkey)
    print(donkey_with_saddle.drive(country_road))


    # Мы можем использовать адаптированного осла везде, где ожидается Transport
    def travel(transport: Transport, road: Road):
        return transport.drive(road)


    print(travel(car, highway))
    print(travel(donkey_with_saddle, country_road))