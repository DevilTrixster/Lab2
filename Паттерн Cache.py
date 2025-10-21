class TreeType:
    """Внутреннее состояние (разделяемое) - тип дерева"""

    def __init__(self, name, color, texture):
        self.name = name
        self.color = color
        self.texture = texture

    def display(self, x, y, size):
        print(f"Отображаем {self.name} дерево ({self.color}, {self.texture}) "
              f"в позиции ({x}, {y}) размером {size}")


class TreeFactory:
    """Фабрика-кэш для типов деревьев (Flyweight)"""
    _tree_types = {}

    @classmethod
    def get_tree_type(cls, name, color, texture):
        key = (name, color, texture)
        if key not in cls._tree_types:
            cls._tree_types[key] = TreeType(name, color, texture)
            print(f"Создан новый тип дерева: {name}")
        return cls._tree_types[key]


class Tree:
    """Контекст дерева с внешним состоянием"""

    def __init__(self, x, y, size, tree_type):
        self.x = x
        self.y = y
        self.size = size
        self.tree_type = tree_type  # Ссылка на разделяемый объект

    def display(self):
        self.tree_type.display(self.x, self.y, self.size)


class Forest:
    """Клиентский класс - лес"""

    def __init__(self):
        self.trees = []

    def plant_tree(self, x, y, size, name, color, texture):
        tree_type = TreeFactory.get_tree_type(name, color, texture)
        tree = Tree(x, y, size, tree_type)
        self.trees.append(tree)

    def display_forest(self):
        print(f"\n=== ЛЕС (всего деревьев: {len(self.trees)}) ===")
        for tree in self.trees:
            tree.display()


# Демонстрация работы
if __name__ == "__main__":
    forest = Forest()

    # Сажаем деревья - повторяющиеся типы будут браться из кэша
    forest.plant_tree(10, 20, 5, "Дуб", "зеленый", "грубая")
    forest.plant_tree(30, 40, 3, "Береза", "белый", "гладкая")
    forest.plant_tree(50, 60, 4, "Дуб", "зеленый", "грубая")  # Используем кэш
    forest.plant_tree(70, 80, 6, "Сосна", "темно-зеленый", "игольчатая")
    forest.plant_tree(90, 100, 3, "Береза", "белый", "гладкая")  # Используем кэш
    forest.plant_tree(110, 120, 5, "Дуб", "зеленый", "грубая")  # Используем кэш

    # Отображаем лес
    forest.display_forest()

    # Показываем статистику по использованию памяти
    print(f"\n=== СТАТИСТИКА ===")
    print(f"Всего деревьев: {len(forest.trees)}")
    print(f"Уникальных типов деревьев: {len(TreeFactory._tree_types)}")
    print(f"Экономия памяти: {len(forest.trees) - len(TreeFactory._tree_types)} объектов")