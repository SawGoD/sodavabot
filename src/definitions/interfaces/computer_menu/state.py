class StateInterface:

    def __init__(self, state):
        self.state = state

    @property
    def title(self):
        """Заголовок: 🏃‍♂️ Состояние"""
        return self.state["state"]["title"]

    @property
    def body(self):
        """Тело: Текст"""
        return self.state["state"]["body"]
