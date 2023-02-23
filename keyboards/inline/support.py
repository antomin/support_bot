from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from common.config import SUPPORT_CHAT_ID

support_callback = CallbackData('ask_support', 'user_id', 'as_user')
cancel_support_callback = CallbackData('cancel_support', 'user_id')


async def support_keyboard(user_id=None):
    if user_id:
        contact_id = int(user_id)
        as_user = 'no'
        text = 'Ответить пользователю'
    else:
        contact_id = SUPPORT_CHAT_ID
        as_user = 'yes'

        text = 'Написать в техподдержку'

    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(
        text=text,
        callback_data=support_callback.new(
            user_id=contact_id,
            as_user=as_user
        )
    ))

    keyboard.add(InlineKeyboardButton(
        text='Завершить сеанс',
        callback_data=cancel_support_callback.new(user_id=contact_id)
    ))

    return keyboard


def cancel_support(user_id):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton(
        text='Завершить сеанс',
        callback_data=cancel_support_callback.new(user_id=user_id)
    ))

    return keyboard
