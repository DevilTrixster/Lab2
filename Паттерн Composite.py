from abc import ABC, abstractmethod

class Component(ABC):
    @abstractmethod
    def get_price(self):
        pass

class Product(Component):
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def get_price(self):
        return self.price

class Box(Component):
    def __init__(self, name, packing_cost=0):
        self.name = name
        self.packing_cost = packing_cost
        self.children = []

    def add(self, component):
        self.children.append(component)

    def remove(self, component):
        self.children.remove(component)

    def get_price(self):
        total = self.packing_cost
        for child in self.children:
            total += child.get_price()
        return total


if __name__ == "__main__":
    # Создаем продукты
    phone = Product("Телефон", 22700)
    headphones = Product("Наушники", 4000)
    charger = Product("Зарядка", 500)

    # Создаем маленькую коробку для аксессуаров
    accessories_box = Box("Коробка аксессуаров", 2)
    accessories_box.add(headphones)
    accessories_box.add(charger)

    # Создаем большую коробку для заказа
    main_box = Box("Главная коробка", 5)
    main_box.add(phone)
    main_box.add(accessories_box)

    # Создаем заказ и добавляем в него коробки и продукты
    order = Box("Заказ")  # Упаковка заказа бесплатна
    order.add(main_box)
    order.add(Product("Страхование", 50))

    # Вычисляем общую стоимость заказа
    print(f"Конечная цена заказа: {order.get_price()} руб")