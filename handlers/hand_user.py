from InstanceBot import bot, router, UserStates
from aiogram import types
from database import db
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def start(msg: types.Message, state: FSMContext) -> None:

    bot_name = await bot.get_me()
    user_id = msg.from_user.id
    username = msg.from_user.username
    start_message = msg.text[7:]

    if not db.user_exists(user_id):
        if len(start_message) > 0:
            if start_message.isdigit():

                db.add_user(user_id, ref_id=start_message)

                await bot.send_message(
                    chat_id=start_message,
                    text=f'У Вас новый реферал @{username}!'
                )

        else:
            db.add_user(user_id)

    user_balance = db.get_balance(user_id)

    await msg.answer(f"Приветствую тебя! \nТвоя реферальная ссылка - t.me/{bot_name.username}?start={user_id} \
                    \nТвой баланс: {user_balance} \nДля пополнения баланса - /balance")
    
    await state.set_state(UserStates.test)


async def balance(msg: types.Message, state: FSMContext) -> None:
    user_id = msg.from_user.id
    username = msg.from_user.username
    amount = 10

    db.change_balance(user_id, amount)

    await msg.answer(f"Твой баланс пополнен на {amount} монет!")

    user_referrer = db.get_referrer(user_id)[0]
    while user_referrer and amount > 2:
        amount = amount / 2
        db.change_balance(user_referrer, amount)

        await bot.send_message(user_referrer, f"Твой реферал @{username} получил на баланс {amount * 2} монет, поэтому твой баланс пополнен на {amount} монет!")
        user_referrer = db.get_referrer(user_referrer)[0]
    
    await state.clear()


async def state_test(message: types.Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await message.answer(
        f"Тест репли клавиатуры",
        reply_markup=types.ReplyKeyboardMarkup(
            keyboard=[
                [
                    types.KeyboardButton(text="Yes"),
                    types.KeyboardButton(text="No"),
                ]
            ],
            resize_keyboard=True,
        ),
    )

    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(
        text="GitHub", url="https://github.com")
    )
    builder.row(types.InlineKeyboardButton(
        text="Тест",
        callback_data="test")
    )

    await bot.send_message(
        chat_id=message.from_user.id,
        text=f"Тест инлайн клавиатуры",
        reply_markup=builder.as_markup(),
    )

    await state.set_state(None) # Очистка только состояний без данных


async def callback_handler(call: types.CallbackQuery, state: FSMContext) -> None:

    data = await state.get_data()

    if call.data == 'test':
        await call.message.edit_text("Yes" + data["name"])
    else:
        await call.message.answer("Ошибка")
        
    await state.clear()


def hand_add():
    router.message.register(start, StateFilter(None), CommandStart())
    router.message.register(balance, Command(commands=["balance"]))
    router.message.register(state_test, UserStates.test)
    router.callback_query.register(callback_handler)