class MenuControlsInterface:

    def __init__(self, menu_controls):
        self.menu_controls = menu_controls

    @property
    def update(self):
        """Кнопка: 🔄 Обновить"""
        return self.menu_controls["menu_controls"]["update"]

    @property
    def menu(self):
        """Кнопка: 🔝 Меню"""
        return self.menu_controls["menu_controls"]["menu"]

    @property
    def back(self):
        """Кнопка: 🔙 Назад"""
        return self.menu_controls["menu_controls"]["back"]

    @property
    def expand(self):
        """Кнопка: ◀️"""
        return self.menu_controls["menu_controls"]["expand"]

    @property
    def collapse(self):
        """Кнопка: 🔽"""
        return self.menu_controls["menu_controls"]["collapse"]

    @property
    def filler(self):
        """Заполнитель"""
        return self.menu_controls["menu_controls"]["filler"]
