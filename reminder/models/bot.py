import asyncio

from balebot.updater import Updater

from main_config import BotConfig


class Bot:
    loop = asyncio.get_event_loop()
    updater = Updater(token=BotConfig.bot_token, loop=loop)
    bot = updater.dispatcher.bot
    dispatcher = updater.dispatcher
