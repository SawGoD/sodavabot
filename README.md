# SODA VA BOT v7.25b
<!-- 2023      Март, апрель, май, июнь, июль, август, сентябрь -->
![Typing SVG](https://readme-typing-svg.herokuapp.com?font=Montserrat&weight=500&size=25&duration=2800&pause=800&color=DC143C&vCenter=true&width=500&height=30&lines=S+U+T+I+V+I+S+M+Project.;.)

[![Telegram](https://img.shields.io/badge/SawGoD-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/SawGoD)

---

### Возможности:
> - **Питание ПК:** перезагрузка, гибернация, выключение, отключение мониторов
> - **Буфер обмена:** получение и отправка текста в буфер обмена Windows, обработка ссылок.
> - **Мультимедиа:** управление звука, переключение медиафайлов
> - **Интернет:** измерение скорости сети, VPN подключение
> - **Состояние системы:** мониторинг загруженности CPU, RAM
> - **Скриншоты:** активного приложения, всех или конкретных экранов без сторонних программ

### В планах:
> - **Работа с разными приложениями:** поддержка списка приложений сразу из коробки, без доп. настройки
> - **Chromecast:** поддержка технологии, для вывода изборажения с ПК прямо на телевизор в одно нажатие
> - **Темы:** переключение тем Windows( светлая/тёмная ), расписание для автопереключения
> - **Активные углы:** аналог активных углов MacOS на Windows
> - **Умный дом:** интеграция устройств умного дома с [Алисой](https://yandex.ru/alice/smart-home)

### Недостатки:
> - **Сложность настройки** - на данный момент настройка некоторых функций происходит напрямую в коде, в разных его участках. Это неправильно и будет меняться.
> - **Отсутствие Plug&Play** - проблема из предыдущего пункта. Бот изнечально создавался только для личного использования, для конкретных задач и приложений, в будущем будет добавлена гибкость.

---

## Установка: 
1. Git Bash:

    1.1 Выполните команду: 
    
    ```bash
    git clone https://github.com/SawGoD/sodavabot C:/Soda_VA_BOT
    ```
    1.2 Запустите файл **install.bat** от имени администратора. 

    1.3 Настройте основные параметры **.env**    
    
    1.4 Запустите **soda_va_bot_start.bat** или **soda_local.bat**
    - _Мы создаём папку, чтобы автозапуск и обновления работали корректно_
    - _Обновление происходит автоматически_

2. Архив: 

    1.1 Скачайте [архив](https://github.com/SawGoD/sodavabot/archive/refs/heads/main.zip)
    
    1.2 Распакуйте архив в любое место

    1.3 Запустите файл **install.bat** от имени администратора

    1.4 Настройте основные параметры **.env**
    
    1.5 Запустите **soda_va_bot_start.bat** или **soda_local.bat**    
    - _Обновление происходит мануально_


### Основные параметры .env:

`BOT_TOKEN=replace` - Токен телеграм бота

`ALLOWED_USERS={'replace'}` - ID пользователей, которые имеют доступ к боту

`ADMIN_USERS={'replace'}` - ID администраторов

`LOG_IGNORED_USERS={'replace'}` - ID пользователей, которые не будут записываться в лог

`LOG_OUTPUT=replace` - ID группы для отправки логов

### Дополнительные параметры .env:

`LOG_ALERT={'screen', 'logger'}` - Переменные callback_data для отправки логов с высоким приоритетом

`STEAM_LOGIN=replace` - Логин для Steam

`STEAM_PASS=replace` - Пароль для Steam

`API_TOKEN_GIT=unavailable` - Token для получения списка изменений из GitHub, для разработчика

`API_TOKEN=replace`- Placeholder для будущих/возможных изменений

---

<!-- #### Список основных callback_data:
<details>
    <summary>Раскрыть</summary>

|Название|Описание|
|--------|--------|
|`logger`|Отвечает за включение или отключение логов|
|`sounds`|Отвечает за включение или отключение звуков|
|`hints`|Отвечает за включение или отключение подсказок|
|`screen`|Отвечает за открытие меню скриншотов|
|`scrn_full`|Делает скриншот всех доступных экранов|
|`scrn_mon`|Делает скриншот активного экрана|
|`scrn_app`|Делает скриншот активного приложения|
</details> -->

#### Библиотеки:
<details>
    <summary>Раскрыть</summary>

|Название|Описание|
|--------|--------|
|telegram-bot|Это библиотека для создания ботов в Telegram. Она предоставляет функциональность для работы с API Telegram, обработки входящих сообщений и отправки сообщений от бота.|
|telegram|Это библиотека для работы с Telegram API. Она предоставляет набор методов для отправки сообщений, создания групп и каналов, управления пользователями и других операций.|
|telegram.ext|Это расширение библиотеки telegram, которое предоставляет дополнительные функции и возможности для создания ботов в Telegram. Оно включает в себя поддержку обработки команд, клавиатур, инлайн-кнопок и других функций.|
|pyautogui|Это библиотека для автоматизации действий на компьютере. Она позволяет программно управлять мышью и клавиатурой, осуществлять снимки экрана, взаимодействовать с окнами и элементами интерфейса других приложений и многое другое.|
|pyperclip|Это библиотека для работы с буфером обмена. Она позволяет копировать и вставлять текст из буфера обмена, а также работать с изображениями и файлами.|
|dotenv|Это библиотека для загрузки переменных окружения из файла .env. Она позволяет хранить конфиденциальную информацию, такую как токены и ключи доступа, в файле .env, который не попадает в систему контроля версий.|
|pyglet|Это библиотека для создания графических и звуковых приложений. Она предоставляет возможности для отображения графики, воспроизведения звука и видео, обработки пользовательского ввода и других функций.|
|mss|Это библиотека для захвата снимков экрана с помощью Python|
|pygetwindow|Это библиотека для работы с окнами и элементами интерфейса других приложений|
</details>

---

#### Благодарность:
> - [**RBTray**](https://rbtray.sourceforge.net) - _RBTray это небольшая программа для Windows, которая работает в фоновом режиме и позволяет сворачивать почти любое окно в системный трей, щелкнув правой кнопкой мыши на кнопке сворачивания._
> - [**NirCmd**](https://www.nirsoft.net/utils/nircmd.html) - _NirCmd это небольшая утилита командной строки, которая позволяет выполнять полезные задачи без отображения пользовательского интерфейса._
> - [**SoundVolumeView**](https://www.nirsoft.net/utils/sound_volume_view.html) - _SoundVolumeView это простой инструмент для Windows Vista/7/8/2008/10/11, который отображает общую информацию и текущий уровень громкости для всех активных звуковых компонентов на вашей системе и позволяет мгновенно выключать и включать их._
> - [**SoundVolumeCommandLine**](https://www.nirsoft.net/utils/sound_volume_command_line.html) - _SoundVolumeCommandLine это инструмент командной строки для управления громкостью звука. Он предоставляет различные действия, такие как установка громкости, включение/выключение звука, увеличение/уменьшение громкости и другие._
> - [**SetVol**](https://www.rlatour.com/setvol/) - _SetVol это бесплатная утилита командной строки с открытым исходным кодом, которая позволяет устанавливать уровень громкости и записи аудио- и записывающих устройств вашего компьютера под управлением Windows._
> - [**@bukomp**](https://github.com/bukomp) aka Edvard Shalaev

---

#### Совместимость:
![Windows](https://img.shields.io/badge/Windows%2010/11-%230079d5.svg?style=for-the-badge&logo=Windows%2011&logoColor=white)