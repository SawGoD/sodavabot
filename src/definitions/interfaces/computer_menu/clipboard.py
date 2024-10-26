class ClipboardInterface:

    def __init__(self, clipboard):
        self.clipboard = clipboard

    @property
    def title(self):
        """Заголовок: 📋 Буфер обмена"""
        return self.clipboard["clipboard"]["title"]

    @property
    def body(self):
        """Тело: Текст"""
        return self.clipboard["clipboard"]["body"]
