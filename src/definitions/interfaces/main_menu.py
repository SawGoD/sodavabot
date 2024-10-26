class MainMenuInterface:

    def __init__(self, menu):
        self.menu = menu

    @property
    def title(self):
        """Заголовок: Меню"""
        return self.menu["main_menu"]["title"]

    @property
    def no_access(self):
        """Заголовок: У Вас нет доступа"""
        return self.menu["main_menu"]["title_no_access"]

    @property
    def apps(self):
        """Заголовок: 📟 Приложения"""
        return self.menu["main_menu"]["apps"]

    @property
    def computer(self):
        """Заголовок: 🖥 Компьютер"""
        return self.menu["main_menu"]["computer"]

    @property
    def settings(self):
        """Заголовок: ⚙ Настройки"""
        return self.menu["main_menu"]["settings"]
