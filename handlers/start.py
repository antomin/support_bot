from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from common.variables import START_MSG
from loader import dp


@dp.message_handler(Command('start'))
async def start(message: Message):
    await message.answer(START_MSG)