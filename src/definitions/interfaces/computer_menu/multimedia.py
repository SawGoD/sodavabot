class MultimediaInterface:

    def __init__(self, multimedia):
        self.multimedia = multimedia

    @property
    def title(self):
        """Заголовок: 🔂 Мультимедиа"""
        return self.multimedia["multimedia"]["title"]

    @property
    def body(self):
        """Тело: Текст"""
        return self.multimedia["multimedia"]["body"]

    @property
    def volup(self):
        """Кнопка: ➕"""
        return self.multimedia["multimedia"]["menu"]["volup"]

    @property
    def voldowm(self):
        """Кнопка: ➖"""
        return self.multimedia["multimedia"]["menu"]["voldowm"]

    @property
    def volon(self):
        """Кнопка: 🔊"""
        return self.multimedia["multimedia"]["menu"]["volon"]

    @property
    def voloff(self):
        """Кнопка: 🔇"""
        return self.multimedia["multimedia"]["menu"]["voloff"]

    @property
    def playpause(self):
        """Кнопка: ⏯"""
        return self.multimedia["multimedia"]["menu"]["playpause"]

    @property
    def previous(self):
        """Кнопка: ⏮️"""
        return self.multimedia["multimedia"]["menu"]["previous"]

    @property
    def next(self):
        """Кнопка: ⏭️"""
        return self.multimedia["multimedia"]["menu"]["next"]
