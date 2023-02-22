from aiogram.types import BotCommand


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        BotCommand('start', 'Запустить бота'),
        BotCommand('support', 'Написать сообщение в техподдержку'),
        BotCommand('help', 'Помощь'),
    ])
