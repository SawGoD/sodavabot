from definitions.interfaces.computer_menu.clipboard import ClipboardInterface
from definitions.interfaces.computer_menu.multimedia import MultimediaInterface
from definitions.interfaces.computer_menu.power import PowerInterface
from definitions.interfaces.computer_menu.screen import ScreenInterface
from definitions.interfaces.computer_menu.state import StateInterface
from definitions.models.computer_menu.clipboard import clipboard as clipboard_model
from definitions.models.computer_menu.multimedia import multimedia as multimedia_model
from definitions.models.computer_menu.power import power as power_model
from definitions.models.computer_menu.screen import screen as screen_model
from definitions.models.computer_menu.state import state as state_model

multimedia = MultimediaInterface(multimedia_model)
"""
Конфигурация интерфейса "Мультимедиа"
"""

screen = ScreenInterface(screen_model)
"""
Конфигурация интерфейса "Экран"   
"""

clipboard = ClipboardInterface(clipboard_model)
"""
Конфигурация интерфейса "Буфер обмена"
"""

state = StateInterface(state_model)
"""
Конфигурация интерфейса "Состояние"
"""

power = PowerInterface(power_model)
"""
Конфигурация интерфейса "Питание"
"""
