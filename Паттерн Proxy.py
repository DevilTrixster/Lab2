from abc import ABC, abstractmethod
import time


# Интерфейс сервиса изображений (аналог IImage в .NET)
class IImageService(ABC):
    @abstractmethod
    def display(self) -> str:
        pass


# Реальный сервис загрузки изображений
class HighResolutionImage(IImageService):
    def __init__(self, filename: str):
        self._filename = filename
        self._load_image_from_disk()

    def _load_image_from_disk(self):
        print(f"Загрузка высококачественного изображения {self._filename}...")
        time.sleep(3)  # Имитация долгой загрузки
        print("Изображение загружено!")

    def display(self) -> str:
        return f"Отображение высококачественного изображения: {self._filename}"


# Proxy для ленивой загрузки и контроля доступа
class ImageProxy(IImageService):
    def __init__(self, filename: str, user_role: str = "User"):
        self._filename = filename
        self._user_role = user_role
        self._real_image = None

    def display(self) -> str:
        # Проверка прав доступа
        if self._user_role not in ["Admin", "User"]:
            raise PermissionError("Недостаточно прав для просмотра изображения")

        # Ленивая загрузка
        if self._real_image is None:
            self._real_image = HighResolutionImage(self._filename)

        # Дополнительная логика
        print(f"[PROXY] Логирование доступа пользователя {self._user_role}")

        return self._real_image.display()


# Демонстрация
def main():
    print("=== ДЕМОНСТРАЦИЯ PATTERN PROXY ===\n")

    # Создаем прокси (изображение НЕ загружается сразу)
    print("1. Создание ImageProxy...")
    image_proxy = ImageProxy("photo.jpg", "User")

    print("\n2. Первый вызов display() - происходит загрузка:")
    result1 = image_proxy.display()
    print(f"Результат: {result1}")

    print("\n3. Второй вызов display() - используется кэш:")
    result2 = image_proxy.display()
    print(f"Результат: {result2}")

    print("\n4. Попытка доступа без прав:")
    try:
        bad_proxy = ImageProxy("secret.jpg", "Guest")
        bad_proxy.display()
    except PermissionError as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()