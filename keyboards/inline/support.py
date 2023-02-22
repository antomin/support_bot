import random

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from common.config import support_ids
from loader import dp

support_callback = CallbackData('ask_support', 'user_id', 'as_user')
cancel_support_callback = CallbackData('cancel_support', 'user_id')


async def check_support_available(support_id):
    state = dp.current_state(chat=support_id, user=support_id)
    state_str = str(await state.get_state())

    return support_id if state_str != 'in_support' else None


async def get_support_manager():
    random.shuffle(support_ids)
    for support_id in support_ids:
        support_id = await check_support_available(support_id)
        if support_id:
            return support_id
    return


async def support_keyboard(user_id=None):
    if user_id:
        contact_id = int(user_id)
        as_user = 'no'
        text = 'Ответить пользователю'
    else:
        contact_id = await get_support_manager()
        as_user = 'yes'

        if not contact_id:
            return False

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
