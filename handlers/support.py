from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, ContentTypes, Message

from keyboards.inline.support import support_callback, support_keyboard
from loader import dp


@dp.message_handler(Command('support'))
async def ask_support(message: Message):
    text = 'Хотите написать сообщение техподдержке?\nНажмите на кнопку ниже!'
    keyboard = await support_keyboard(messages='one')

    await message.answer(text=text, reply_markup=keyboard)


@dp.callback_query_handler(support_callback.filter(messages='one'))
async def send_to_support(call: CallbackQuery, state: FSMContext, callback_data: dict):
    await call.answer()
    user_id = int(callback_data.get('user_id'))

    await call.answer('Пришлите Ваше сообщение для техподдержки:')
    await state.set_state('waiting_support_answer')
    await state.update_data(second_id=user_id)


@dp.message_handler(state='waiting_support_answer', content_types=ContentTypes.ANY)
async def get_support_message(message: Message, state: FSMContext):
    data = await state.get_data()
    second_id = data.get('second_id')

    await dp.bot.send_message(chat_id=second_id, text='Вам сообщение.\n Вы можете ответить, нажав на кнопку ниже.')

    keyboard = await support_keyboard(messages='one', user_id=message.from_user.id)

    await message.copy_to(second_id, reply_markup=keyboard)

    await message.answer('Вы отправили это сообщение!')

    await state.reset_state()