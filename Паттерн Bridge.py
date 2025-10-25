from abc import ABC, abstractmethod
from datetime import datetime

# Реализация (Implementor) - интерфейс для различных способов логирования
class LoggerImplementation(ABC):
    @abstractmethod
    def log_message(self, message: str, level: str):
        pass

# Конкретные реализации логирования
class ConsoleLogger(LoggerImplementation):
    def log_message(self, message: str, level: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {message}")

class FileLogger(LoggerImplementation):
    def __init__(self, filename: str = "shop.log"):
        self.filename = filename

    def log_message(self, message: str, level: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.filename, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] [{level}] {message}\n")

class DatabaseLogger(LoggerImplementation):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        # Здесь была бы реальная инициализация подключения к БД

    def log_message(self, message: str, level: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # В реальной реализации здесь был бы код записи в БД
        print(f"DB LOG [{timestamp}] [{level}] {message}")

# Абстракция (Abstraction) - базовый класс логирования для интернет-магазина
class ShopLogger:
    def __init__(self, implementation: LoggerImplementation):
        self._implementation = implementation

    def log(self, message: str, level: str):
        self._implementation.log_message(message, level)

    def info(self, message: str):
        self.log(message, "INFO")

    def warning(self, message: str):
        self.log(message, "WARNING")

    def error(self, message: str):
        self.log(message, "ERROR")


# Расширенная абстракция (Refined Abstraction) - логирование с дополнительным контекстом
class ContextShopLogger(ShopLogger):
    def __init__(self, implementation: LoggerImplementation, context: str):
        super().__init__(implementation)
        self.context = context

    def log(self, message: str, level: str):
        enriched_message = f"[{self.context}] {message}"
        super().log(enriched_message, level)

    def log_user_action(self, user_id: int, action: str):
        self.info(f"Пользователь {user_id} исполняется: {action}")

    def log_purchase(self, user_id: int, order_id: int, amount: float):
        self.info(f"Пользователь {user_id} заказывает покупку {order_id} за {amount:.2f} руб")


# Еще одна расширенная абстракция - логирование с производительностью
class PerformanceShopLogger(ShopLogger):
    def log_performance(self, operation: str, execution_time: float):
        level = "WARNING" if execution_time > 1.0 else "INFO"
        self.log(f"Операция '{operation}' выполняется за {execution_time:.3f}s", level)

if __name__ == "__main__":
    # Создаем различные реализации логирования
    console_logger = ConsoleLogger()
    file_logger = FileLogger("ecommerce.log")
    db_logger = DatabaseLogger("postgresql://localhost/shop")

    print("=== Базовое логирование ===")
    basic_logger = ShopLogger(console_logger)
    basic_logger.info("Магазин запущен")
    basic_logger.warning("Низкий запас товара X")
    basic_logger.error("Ошибка подключения к платежной системе")

    print("\n=== Логирование с контекстом ===")
    user_logger = ContextShopLogger(file_logger, "USER")
    order_logger = ContextShopLogger(db_logger, "ORDER")

    user_logger.log_user_action(123, "login")
    user_logger.log_user_action(123, "add_to_cart")
    order_logger.log_purchase(123, 4567, 149.99)

    print("\n=== Производительность ===")
    perf_logger = PerformanceShopLogger(console_logger)
    perf_logger.log_performance("Обработка заказа", 0.245)
    perf_logger.log_performance("Генерация отчета", 2.134)

    print("\n=== Динамическая смена реализации ===")
    # Можно менять реализацию на лету
    dynamic_logger = ShopLogger(console_logger)
    dynamic_logger.info("Логируем в консоль")

    # Переключаемся на файловое логирование
    dynamic_logger._implementation = file_logger
    dynamic_logger.info("Теперь логируем в файл")

    # Переключаемся на БД
    dynamic_logger._implementation = db_logger
    dynamic_logger.info("И теперь в базу данных")
