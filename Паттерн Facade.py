from abc import ABC, abstractmethod
from typing import Dict, Any, List

class UserDatabase:
    """Сложная подсистема для работы с базой данных пользователей"""

    def __init__(self):
        self._connection = "PostgreSQL Connection - Users"
        self._users = [
            {"id": 1, "name": "Виктор Иосович", "email": "Victor@mail.ru"},
            {"id": 2, "name": "Владислав Сенчилов", "email": "Senchilov@mail.ru"}
        ]

    def connect(self):
        print(f"Подключение к базе пользователей: {self._connection}")
        return True

    def disconnect(self):
        print("Отключение от базы пользователей")

    def execute_query(self, query: str):
        print(f"Выполнение запроса к базе пользователей: {query}")
        # Здесь была бы реальная логика выполнения запроса
        return f"Результат из базы пользователей: {query}"

    def get_user_by_id(self, user_id: int) -> Dict[str, Any]:
        print(f"Поиск пользователя с ID: {user_id}")
        for user in self._users:
            if user["id"] == user_id:
                return user
        return {}

    def get_all_users(self) -> List[Dict[str, Any]]:
        print("Получение всех пользователей")
        return self._users

    def create_user(self, name: str, email: str) -> Dict[str, Any]:
        print(f"Создание пользователя: {name}, {email}")
        new_id = max(user["id"] for user in self._users) + 1
        new_user = {"id": new_id, "name": name, "email": email}
        self._users.append(new_user)
        return new_user


class OrderDatabase:
    """Сложная подсистема для работы с базой данных заказов"""

    def __init__(self):
        self._connection = "MongoDB Connection - Orders"
        self._orders = [
            {"id": 101, "user_id": 1, "product": "Ноутбук", "amount": 15975},
            {"id": 102, "user_id": 2, "product": "Телефон", "amount": 8755}
        ]

    def connect(self):
        print(f"Подключение к базе заказов: {self._connection}")
        return True

    def disconnect(self):
        print("Отключение от базы заказов")

    def execute_query(self, query: str):
        print(f"Выполнение запроса к базе заказов: {query}")
        # Здесь была бы реальная логика выполнения запроса
        return f"Результат из базы заказов: {query}"

    def get_order_by_id(self, order_id: int) -> Dict[str, Any]:
        print(f"Поиск заказа с ID: {order_id}")
        for order in self._orders:
            if order["id"] == order_id:
                return order
        return {}

    def get_orders_by_user(self, user_id: int) -> List[Dict[str, Any]]:
        print(f"Поиск заказов пользователя с ID: {user_id}")
        return [order for order in self._orders if order["user_id"] == user_id]

    def create_order(self, user_id: int, product: str, amount: float) -> Dict[str, Any]:
        print(f"Создание заказа для пользователя {user_id}: {product}")
        new_id = max(order["id"] for order in self._orders) + 1
        new_order = {"id": new_id, "user_id": user_id, "product": product, "amount": amount}
        self._orders.append(new_order)
        return new_order


class AnalyticsDatabase:
    """Дополнительная сложная подсистема для аналитики"""

    def __init__(self):
        self._connection = "Elasticsearch Connection - Analytics"

    def connect(self):
        print(f"Подключение к базе аналитики: {self._connection}")
        return True

    def disconnect(self):
        print("Отключение от базы аналитики")

    def log_user_activity(self, user_id: int, action: str):
        print(f"Логирование активности пользователя {user_id}: {action}")
        return f"Активность записана: пользователь {user_id} - {action}"

    def get_user_statistics(self, user_id: int) -> Dict[str, Any]:
        print(f"Получение статистики для пользователя {user_id}")
        return {
            "user_id": user_id,
            "total_orders": 5,  # Примерные данные
            "total_spent": 1250.50,
            "favorite_category": "Electronics"
        }


# Фасад - единый интерфейс для работы со всеми базами данных
class DatabaseFacade:
    """
    Фасад, скрывающий сложность работы с несколькими базами данных
    и предоставляющий простой единый интерфейс
    """

    def __init__(self):
        self._user_db = UserDatabase()
        self._order_db = OrderDatabase()
        self._analytics_db = AnalyticsDatabase()

        # Автоматическое подключение ко всем базам при инициализации
        self._initialize_connections()

    def _initialize_connections(self):
        print("Инициализация подключений к базам данных...")
        self._user_db.connect()
        self._order_db.connect()
        self._analytics_db.connect()
        print("Все подключения установлены\n")

    def close_connections(self):
        print("Закрытие подключений к базам данных...")
        self._user_db.disconnect()
        self._order_db.disconnect()
        self._analytics_db.disconnect()
        print("Все подключения закрыты")

    # Упрощенные методы для клиентского кода

    def get_user_profile(self, user_id: int) -> Dict[str, Any]:
        """Получить полный профиль пользователя с заказами и статистикой"""
        print(f"Получение полного профиля пользователя {user_id}")

        # Работа с разными базами скрыта внутри фасада
        user = self._user_db.get_user_by_id(user_id)
        orders = self._order_db.get_orders_by_user(user_id)
        statistics = self._analytics_db.get_user_statistics(user_id)

        return {
            "user_info": user,
            "orders": orders,
            "statistics": statistics
        }

    def create_user_order(self, user_id: int, product: str, amount: float) -> Dict[str, Any]:
        """Создать заказ для пользователя с полной логикой"""
        print(f"Создание заказа для пользователя {user_id}")

        # Проверяем существование пользователя
        user = self._user_db.get_user_by_id(user_id)
        if not user:
            raise ValueError(f"Пользователь с ID {user_id} не найден")

        # Создаем заказ
        order = self._order_db.create_order(user_id, product, amount)

        # Логируем активность
        self._analytics_db.log_user_activity(user_id, f"Создан заказ {order['id']}")

        return {
            "success": True,
            "order": order,
            "user": user
        }

    def register_new_user(self, name: str, email: str) -> Dict[str, Any]:
        """Зарегистрировать нового пользователя"""
        print(f"Регистрация нового пользователя: {name}")

        user = self._user_db.create_user(name, email)
        self._analytics_db.log_user_activity(user["id"], "Регистрация")

        return {
            "success": True,
            "user": user,
            "message": f"Пользователь {name} успешно зарегистрирован"
        }

    def get_system_report(self) -> Dict[str, Any]:
        """Получить системный отчет из всех баз данных"""
        print("Формирование системного отчета...")

        users = self._user_db.get_all_users()
        total_users = len(users)

        # Собираем информацию о заказах
        total_orders = 0
        total_revenue = 0.0

        for user in users:
            user_orders = self._order_db.get_orders_by_user(user["id"])
            total_orders += len(user_orders)
            total_revenue += sum(order["amount"] for order in user_orders)

        return {
            "total_users": total_users,
            "total_orders": total_orders,
            "total_revenue": total_revenue,
            "average_order_value": total_revenue / total_orders if total_orders > 0 else 0
        }


# Клиентский код, который использует фасад
def main():
    # Клиент работает только с фасадом, не зная о сложной системе
    db_facade = DatabaseFacade()

    try:
        print("=== ДЕМОНСТРАЦИЯ РАБОТЫ ФАСАДА ===\n")

        # 1. Получение профиля пользователя
        print("1. Получение профиля пользователя:")
        profile = db_facade.get_user_profile(1)
        print(f"Профиль: {profile}\n")

        # 2. Создание нового заказа
        print("2. Создание нового заказа:")
        new_order = db_facade.create_user_order(2, "Ноутбук", 299.99)
        print(f"Новый заказ: {new_order}\n")

        # 3. Регистрация нового пользователя
        print("3. Регистрация нового пользователя:")
        new_user = db_facade.register_new_user("Алексей Жарков", "Jarkov@mail.ru")
        print(f"Новый пользователь: {new_user}\n")

        # 4. Получение системного отчета
        print("4. Системный отчет:")
        report = db_facade.get_system_report()
        for key, value in report.items():
            print(f"  {key}: {value}")
        print()

        # 5. Создание заказа для нового пользователя
        print("5. Создание заказа для нового пользователя:")
        order_for_new_user = db_facade.create_user_order(3, "Наушники", 99.99)
        print(f"Заказ: {order_for_new_user}\n")

    finally:
        # Всегда закрываем соединения
        db_facade.close_connections()


# Альтернативное использование - специализированные фасады
class ReadOnlyDatabaseFacade:
    """Специализированный фасад только для операций чтения"""

    def __init__(self):
        self._user_db = UserDatabase()
        self._order_db = OrderDatabase()
        self._analytics_db = AnalyticsDatabase()
        self._initialize_connections()

    def _initialize_connections(self):
        self._user_db.connect()
        self._order_db.connect()
        self._analytics_db.connect()

    def get_user_data(self, user_id: int):
        user = self._user_db.get_user_by_id(user_id)
        orders = self._order_db.get_orders_by_user(user_id)
        stats = self._analytics_db.get_user_statistics(user_id)
        return {"user": user, "orders": orders, "stats": stats}

    def close(self):
        self._user_db.disconnect()
        self._order_db.disconnect()
        self._analytics_db.disconnect()


if __name__ == "__main__":
    main()

    print("\n" + "=" * 50)
    print("ДЕМОНСТРАЦИЯ СПЕЦИАЛИЗИРОВАННОГО ФАСАДА")
    print("=" * 50)

    # Использование специализированного фасада
    read_only_facade = ReadOnlyDatabaseFacade()
    try:
        user_data = read_only_facade.get_user_data(1)
        print(f"Данные пользователя (только чтение): {user_data}")
    finally:
        read_only_facade.close()