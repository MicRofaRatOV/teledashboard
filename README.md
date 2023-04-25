# 📊 TeleDashBoard

## Info
An interactive online board for media playback in your browser, controlled by your telegram

Main bot: [@tele_dash_board_bot] (RU) [site](https://teledashboard.mf47.ru/)

## Installation
### Preparation
1. Move all files from **/src** folder to **/your/folder/name**
2. Create /your/folder/name/.**deleted**
3. Copy /your/folder/name/db/**empty\_DBNAME**.**db** to /your/folder/name/db/**DBNAME**.**db**
4. Create file /your/folder/name/telegram/**telegram\_token**.**py** with the following content:
```python
# Your telegram token
TOKEN = "1111111111:to-kE_n"
```
5. Configure /your/folder/name/telegram/**server\_info**.**py** file
6. Configure /your/folder/name/php_root/**vars.php** file
7. *OPTIONAL*. You can configure /your/folder/name/**statistics.py**

### Python
1. Install [python 3.11]
2. Install `pyTelegramBotAPI`, `colorama` using [pip] (my testing version of pyTelegramBotAPI is 4.10.0)
```sh
python3.11 -m pip install pyTelegramBotAPI colorama
```
3. *OPTIONAL*. You can change locale (defalut: ru\_RU) here: /your/folder/name/telegram/**messages**.**py** if your locale file exists here: /your/folder/name/telegram/**localization**/**xx\_XX**.**py**
4. Run TelegramBot: 
```sh
python3.11 /your/folder/name/telegram/main_tgbot.py
```

### PHP
- Install [PHP] on your PC or Server
- Just mark /your/folder/name/**php\_root** as the root of your server, but not below this directory!

## Built-in programs
### kEditor
Simple adminpanel key editor, requiring `colorama`. Used to generate and manage access keys for your adminpanel
```sh
# start kEditor
python3.11 /your/folder/name/kEditor.py
```

## Starting server
1. Run php server
2. Run statistics updater
```sh
# Running stat updater
python3.11 /your/folder/name/statistics.py
```
3. Run TelegramBot
```sh
# Running main telegram bot
python3.11 /your/folder/name/telegram/main_tgbot.py
```
4. *OPTIONAL*. Run aminpanel key etditor to update access keys
```sh
python3.11 /your/folder/name/kEditor.py
```
## License

[MIT](https://github.com/MicRofaRatOV/teledashboard/blob/master/LICENSE)

[python 3.11]: <https://docs.python.org/3.11/using/index.html>
[DB Browser for SQLite]: <https://sqlitebrowser.org/dl/>
[pip]: <https://pypi.org/project/pip/>
[PHP]: <https://www.php.net/downloads.php>
[@tele_dash_board_bot]: <https://t.me/tele_dash_board_bot>
