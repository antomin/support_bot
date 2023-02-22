import random

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from common.config import support_ids
from loader import dp

support_callback = CallbackData('ask_support', 'messages', 'user_id', 'as_user')
cancel_support = CallbackData('cancel_support', 'user_id')


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

async def support_keyboard(messages, user_id=None):
    if user_id:
        contact_id = int(user_id)
        as_user = 'no'
        text = 'Ответить пользователю'
    else:
        contact_id = await get_support_manager()
        as_user = 'yes'
        if messages == 'meny' and not contact_id:
            return False
        elif messages == 'one' and not contact_id:
            contact_id = random.choice(support_ids)
        text = 'Написать 1 сообщение в техподдержку' if messages == 'one' else 'Написать в техподдержку'

    keyboard = InlineKeyboardMarkup()

    keyboard.add(InlineKeyboardButton(
        text=text,
        callback_data=support_callback.new(
            messages=messages,
            user_id=contact_id,
            as_user=as_user
        )
    ))

    if messages == 'many':
        keyboard.add(InlineKeyboardButton(
            text='Завершить сеанс',
            callback_data=cancel_support.new(user_id=contact_id)
        ))

    return keyboard
