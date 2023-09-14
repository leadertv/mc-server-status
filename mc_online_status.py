# Не забудь установить зависимости
# pip install requests
# pip install python-telegram-bot==13.7.0
#
# Для работы на VDS после закрытия терминала, вам понадобится программа screen
# Желательно запускать код в изолированной среде venv 

import requests
from telegram import Bot
from telegram.ext import CommandHandler, Updater
from telegram.ext.dispatcher import run_async
from datetime import datetime, timedelta

# Получите токен в https://t.me/BotFather
bot_token = 'ТОКЕН БОТА ТЕЛЕГРАМ'


# Здесь список серверов Minecraft IP и ПОРТ Например 'Hi-Tech': '192.38.00.55:25568'
servers = {
    'Hi-Tech': 'IP:PORT',
    'Techno-Magic': 'IP:PORT',
    'Survival': 'IP:PORT',
    'Server4': 'IP:PORT'
}

cooldowns = {}


# Обработчик команды '/status'

@run_async
def status(update, context):
    chat_id = update.effective_chat.id

    if chat_id not in cooldowns:
        cooldowns[chat_id] = datetime.now() - timedelta(seconds=31)

    #КД на команду в 30 сек чтобы не спамили
    cooldown = cooldowns[chat_id]
    diff = datetime.now() - cooldown

    if diff.total_seconds() < 30:
        context.bot.send_message(chat_id=chat_id, text="Подождите еще {} секунд перед использованием команды /status.".format(int(30 - diff.total_seconds())))
        return

    server_status = []
    total_online = 0

    for server_name, server_address in servers.items():
        try:
            # Отправляем запрос к серверу, чтобы получить данные онлайна и собираем ответ
            response = requests.get(f"https://api.mcsrvstat.us/2/{server_address}")
            response_json = response.json()
            online_players = response_json['players']['online']
            server_status.append(f"{server_name}: {online_players} игроков онлайн")
            total_online += online_players
        except:
            # Если возникает ошибка при получении данных, то значит не судьба
            server_status.append(f"Ошибка при получении информации о сервере {server_name}")

    server_status.append("")
    server_status.append(f"Общий онлайн: {total_online} игроков")
    message = "\n".join(server_status)
    context.bot.send_message(chat_id=chat_id, text=message)
    cooldowns[chat_id] = datetime.now()

updater = Updater(token=bot_token, use_context=True)
status_handler = CommandHandler('status', status)
updater.dispatcher.add_handler(status_handler)


# Стартуем!
updater.start_polling()