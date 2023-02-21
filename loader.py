from aiogram import Bot, Dispatcher

from common.settings import TG_TOKEN

bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot=bot)
