class PowerInterface:

    def __init__(self, power):
        self.power = power

    @property
    def title(self):
        """Заголовок: ⚠ Питание"""
        return self.power["power"]["title"]

    @property
    def body(self):
        """Тело: Текст"""
        return self.power["power"]["body"]
