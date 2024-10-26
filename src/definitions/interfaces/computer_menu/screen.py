class ScreenInterface:

    def __init__(self, screen):
        self.screen = screen

    @property
    def title(self):
        """Заголовок: 📷 Экран"""
        return self.screen["screen"]["title"]

    @property
    def body(self):
        """Тело: Текст"""
        return self.screen["screen"]["body"]
