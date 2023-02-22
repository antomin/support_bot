from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, ContentTypes, Message

from keyboards.inline.support import (cancel_support, cancel_support_callback,
                                      check_support_available,
                                      get_support_manager, support_callback,
                                      support_keyboard)
from loader import dp


@dp.message_handler(Command('support'))
async def ask_support(message: Message):
    text = 'Для связи с техподдержкой нажмите на кнопку ниже.'
    keyboard = await support_keyboard()

    await message.answer(text=text, reply_markup=keyboard)


@dp.callback_query_handler(support_callback.filter(as_user='yes'))
async def send_to_support_call(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await call.message.edit_text('Ваше сообщение отправлено. Ждём ответа от оператора...')

    user_id = int(callback_data.get('user_id'))

    support_id = await get_support_manager() if not await check_support_available(user_id) else user_id

    if not support_id:
        await call.message.edit_text('К сожалению все операторы заняты. Попробуйте позже.')
        await state.reset_state()
        return

    await state.set_state('wait_in_support')
    await state.update_data(second_id=support_id)

    keyboard = await support_keyboard(user_id=call.from_user.id)

    await dp.bot.send_message(
        chat_id=support_id,
        text=f'С Вами хочет связаться пользователь {call.from_user.full_name}',
        reply_markup=keyboard
    )


@dp.callback_query_handler(support_callback.filter(as_user='no'))
async def answer_support_call(call: CallbackQuery, state: FSMContext, callback_data: dict):
    second_id = int(callback_data.get('user_id'))
    user_state = dp.current_state(user=second_id, chat=second_id)

    if str(await user_state.get_state()) != 'wait_in_support':
        await call.message.edit_text('К сожалению пользователь отключился.')

    await state.set_state('in_support')
    await user_state.set_state('in_support')

    await state.update_data(second_id=second_id)

    keyboard = cancel_support(second_id)
    keyboard_second_user = cancel_support(call.from_user.id)

    await call.message.edit_text(
        text='Вы на связи.\nЧтобы завершить сеанс нажмите на кнопку.',
        reply_markup=keyboard
    )

    await dp.bot.send_message(
        chat_id=second_id,
        text='Здравствуйте, мы на связи. Опишите Вашу проблему.',
        reply_markup=keyboard_second_user
    )


@dp.message_handler(state='wait_in_support', content_types=ContentTypes.ANY)
async def not_supported(message: Message, state: FSMContext):
    data = await state.get_data()
    second_id = data.get('second_id')
    keyboard = cancel_support(second_id)

    await message.answer(
        text='Дождитесь ответа оператора или отмените сеанс.',
        reply_markup=keyboard
    )


@dp.callback_query_handler(cancel_support_callback.filter(), state=['in_support', 'wait_in_support', None])
async def exit_support(call: CallbackQuery, state: FSMContext, callback_data: dict):
    user_id = int(callback_data.get('user_id'))
    second_state = dp.current_state(user=user_id, chat=user_id)

    if await second_state.get_state() is not None:
        data_second = await second_state.get_data()
        second_id = data_second.get('second_id')

        if int(second_id) == call.from_user.id:
            await second_state.reset_state()
            await dp.bot.send_message(user_id, 'Пользователь завершил сеанс.')

    await call.message.edit_text('Вы завершили сеанс.')
    await state.reset_state()