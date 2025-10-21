from abc import ABC, abstractmethod
from typing import Dict, Any


# Абстрактный класс системы доставки
class DeliverySystem(ABC):
    @abstractmethod
    def calculate_cost(self, weight: float, distance: float) -> float:
        pass

    @abstractmethod
    def get_delivery_time(self, distance: float) -> int:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass


# Базовые реализации систем доставки
class CourierDelivery(DeliverySystem):
    def calculate_cost(self, weight: float, distance: float) -> float:
        base_cost = 5.0  # Базовая стоимость
        cost_per_km = 0.5
        cost_per_kg = 1.0
        return base_cost + (distance * cost_per_km) + (weight * cost_per_kg)

    def get_delivery_time(self, distance: float) -> int:
        # Стандартное время доставки в днях
        return max(3, int(distance / 50))

    def get_description(self) -> str:
        return "Курьерская доставка"


class PostalDelivery(DeliverySystem):
    def calculate_cost(self, weight: float, distance: float) -> float:
        base_cost = 2.0
        cost_per_kg = 0.5
        return base_cost + (weight * cost_per_kg)

    def get_delivery_time(self, distance: float) -> int:
        # Почта обычно медленнее
        return max(7, int(distance / 30))

    def get_description(self) -> str:
        return "Почтовая доставка"


class PickupDelivery(DeliverySystem):
    def calculate_cost(self, weight: float, distance: float) -> float:
        # Самовывоз обычно бесплатный
        return 0.0

    def get_delivery_time(self, distance: float) -> int:
        # Мгновенная выдача при самовывозе
        return 0

    def get_description(self) -> str:
        return "Самовывоз"


# Класс-потомок для экспресс-доставки (используется в декораторе)
class ExpressDeliverySystem(DeliverySystem):
    def __init__(self):
        self.express_multiplier = 2.0  # Наценка за экспресс
        self.express_time_reduction = 0.3  # Сокращение времени на 30%

    def calculate_cost(self, weight: float, distance: float) -> float:
        # Базовая стоимость экспресс-доставки
        base_express_cost = 10.0
        cost_per_km = 1.0
        return base_express_cost + (distance * cost_per_km)

    def get_delivery_time(self, distance: float) -> int:
        # Экспресс доставка всегда быстрая
        return max(1, int(distance / 100))

    def get_description(self) -> str:
        return "Экспресс-доставка"

    # Специфические методы для экспресс-доставки
    def track_express_shipment(self, tracking_number: str) -> Dict[str, Any]:
        """Заглушка для API отслеживания экспресс-доставки"""
        # В реальной системе здесь был бы вызов API курьерской службы
        return {
            "tracking_number": tracking_number,
            "status": "В пути",
            "estimated_delivery": "Завтра",
            "current_location": "Сортировочный центр",
            "last_update": "2024-01-15 14:30:00"
        }

    def calculate_express_insurance(self, value: float) -> float:
        """Расчет стоимости страховки для экспресс-доставки"""
        return value * 0.02  # 2% от стоимости товара


# Декоратор для добавления функциональности экспресс-доставки
class ExpressDeliveryDecorator(DeliverySystem):
    def __init__(self, wrapped_delivery: DeliverySystem):
        self._wrapped_delivery = wrapped_delivery
        self._express_system = ExpressDeliverySystem()

    def calculate_cost(self, weight: float, distance: float) -> float:
        # Добавляем наценку за экспресс к стоимости базовой доставки
        base_cost = self._wrapped_delivery.calculate_cost(weight, distance)
        express_cost = self._express_system.calculate_cost(weight, distance)
        return base_cost + express_cost * 0.5  # Комбинированная стоимость

    def get_delivery_time(self, distance: float) -> int:
        # Значительно сокращаем время доставки
        base_time = self._wrapped_delivery.get_delivery_time(distance)
        express_time = self._express_system.get_delivery_time(distance)
        return min(base_time, express_time)  # Берем минимальное время

    def get_description(self) -> str:
        return f"{self._wrapped_delivery.get_description()} + Экспресс"

    # Новые методы, добавляемые декоратором
    def track_shipment(self, tracking_number: str) -> Dict[str, Any]:
        """Добавляем возможность отслеживания"""
        return self._express_system.track_express_shipment(tracking_number)

    def get_express_features(self) -> Dict[str, Any]:
        """Получить информацию о экспресс-функциях"""
        return {
            "priority_handling": True,
            "real_time_tracking": True,
            "guaranteed_delivery": True,
            "signature_required": True
        }


# Дополнительные декораторы для специальных услуг
class InsuranceDecorator(DeliverySystem):
    def __init__(self, wrapped_delivery: DeliverySystem, item_value: float):
        self._wrapped_delivery = wrapped_delivery
        self._item_value = item_value

    def calculate_cost(self, weight: float, distance: float) -> float:
        base_cost = self._wrapped_delivery.calculate_cost(weight, distance)
        insurance_cost = self._item_value * 0.01  # 1% страховки
        return base_cost + insurance_cost

    def get_delivery_time(self, distance: float) -> int:
        return self._wrapped_delivery.get_delivery_time(distance)

    def get_description(self) -> str:
        return f"{self._wrapped_delivery.get_description()} + Страховка"


class WeekendDeliveryDecorator(DeliverySystem):
    def __init__(self, wrapped_delivery: DeliverySystem):
        self._wrapped_delivery = wrapped_delivery

    def calculate_cost(self, weight: float, distance: float) -> float:
        base_cost = self._wrapped_delivery.calculate_cost(weight, distance)
        return base_cost + 7.0  # Доплата за доставку в выходные

    def get_delivery_time(self, distance: float) -> int:
        # Гарантируем доставку в выходные
        base_time = self._wrapped_delivery.get_delivery_time(distance)
        return min(base_time, 2)  # Максимум 2 дня

    def get_description(self) -> str:
        return f"{self._wrapped_delivery.get_description()} + Выходные"


# Класс заказа для демонстрации
class Order:
    def __init__(self, items: list, total_value: float, destination_distance: float):
        self.items = items
        self.total_value = total_value
        self.destination_distance = destination_distance
        self.weight = sum(item.get('weight', 0) for item in items)

    def calculate_shipping_options(self, delivery_system: DeliverySystem) -> Dict[str, Any]:
        return {
            "description": delivery_system.get_description(),
            "cost": delivery_system.calculate_cost(self.weight, self.destination_distance),
            "delivery_time": delivery_system.get_delivery_time(self.destination_distance),
            "total_with_shipping": self.total_value + delivery_system.calculate_cost(
                self.weight, self.destination_distance
            )
        }


# Демонстрация работы системы
def main():
    print("=== СИСТЕМА ДОСТАВКИ ИНТЕРНЕТ-МАГАЗИНА ===\n")

    # Создаем тестовый заказ
    order = Order([
        {"name": "Ноутбук", "weight": 2.5, "price": 1000},
        {"name": "Мышь", "weight": 0.2, "price": 50}
    ], total_value=1050, destination_distance=150)

    # Базовые варианты доставки
    courier = CourierDelivery()
    postal = PostalDelivery()
    pickup = PickupDelivery()

    print("БАЗОВЫЕ ВАРИАНТЫ ДОСТАВКИ:")
    print("Курьерская:", order.calculate_shipping_options(courier))
    print("Почтовая:", order.calculate_shipping_options(postal))
    print("Самовывоз:", order.calculate_shipping_options(pickup))

    print("\n" + "=" * 50)
    print("ДОПОЛНИТЕЛЬНЫЕ УСЛУГИ (ДЕКОРАТОРЫ):")
    print("=" * 50)

    # Комбинируем различные варианты доставки с декораторами
    express_courier = ExpressDeliveryDecorator(courier)
    insured_postal = InsuranceDecorator(postal, order.total_value)
    weekend_express = WeekendDeliveryDecorator(express_courier)
    full_service = InsuranceDecorator(weekend_express, order.total_value)

    print("Экспресс-курьер:", order.calculate_shipping_options(express_courier))
    print("Почта со страховкой:", order.calculate_shipping_options(insured_postal))
    print("Экспресс в выходные:", order.calculate_shipping_options(weekend_express))
    print("Полный сервис:", order.calculate_shipping_options(full_service))

    print("\n" + "=" * 50)
    print("ФУНКЦИОНАЛ ЭКСПРЕСС-ДОСТАВКИ:")
    print("=" * 50)

    # Демонстрация специфического функционала экспресс-доставки
    tracking_info = express_courier.track_shipment("TRACK123456")
    print("Отслеживание отправления:", tracking_info)

    express_features = express_courier.get_express_features()
    print("Экспресс-функции:", express_features)

    print("\n" + "=" * 50)
    print("ВСЕ ВОЗМОЖНЫЕ КОМБИНАЦИИ:")
    print("=" * 50)

    # Создаем все возможные комбинации
    delivery_options = [
        ("Простая почта", postal),
        ("Почта + страховка", InsuranceDecorator(postal, order.total_value)),
        ("Курьер", courier),
        ("Курьер + экспресс", express_courier),
        ("Курьер + экспресс + выходные", weekend_express),
        ("Курьер + экспресс + выходные + страховка", full_service),
    ]

    for name, option in delivery_options:
        result = order.calculate_shipping_options(option)
        print(f"{name}: {result}")


# Дополнительный класс для управления доставками
class DeliveryManager:
    def __init__(self):
        self.available_deliveries = {
            "courier": CourierDelivery(),
            "postal": PostalDelivery(),
            "pickup": PickupDelivery()
        }

    def create_custom_delivery(self, base_type: str, options: Dict[str, Any]) -> DeliverySystem:
        """Создать кастомную доставку с выбранными опциями"""
        base_delivery = self.available_deliveries.get(base_type)
        if not base_delivery:
            raise ValueError(f"Unknown delivery type: {base_type}")

        result = base_delivery

        # Применяем декораторы в зависимости от опций
        if options.get("express"):
            result = ExpressDeliveryDecorator(result)

        if options.get("insurance"):
            result = InsuranceDecorator(result, options.get("item_value", 0))

        if options.get("weekend_delivery"):
            result = WeekendDeliveryDecorator(result)

        return result


if __name__ == "__main__":
    main()

    # Демонстрация DeliveryManager
    print("\n" + "=" * 50)
    print("УПРАВЛЕНИЕ ДОСТАВКАМИ ЧЕРЕЗ MANAGER:")
    print("=" * 50)

    manager = DeliveryManager()
    test_order = Order([{"name": "Телефон", "weight": 0.3, "price": 500}], 500, 80)

    # Создаем кастомные доставки
    fast_delivery = manager.create_custom_delivery("courier", {
        "express": True,
        "weekend_delivery": True
    })

    safe_delivery = manager.create_custom_delivery("postal", {
        "insurance": True,
        "item_value": 500
    })

    print("Быстрая доставка:", test_order.calculate_shipping_options(fast_delivery))
    print("Безопасная доставка:", test_order.calculate_shipping_options(safe_delivery))