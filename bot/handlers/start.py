from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
import database.requests as rq
import bot.keyboards.inline as inline
import bot.keyboards.reply as reply
from bot.fsm.register import Register

router = Router()

@router.message(CommandStart())
async def create_user(message: Message):
    user = await rq.get_user(message.from_user.id)
    if user:
        await message.answer(
            f"С возвращением, {user.name}!",
            reply_markup=reply.main_menu(user.role))
    else:
        await message.answer(text="👋 Привет! Выбери роль:", reply_markup=inline.start_message)
@router.callback_query(F.data.startswith('role_'))
async def reg_role(callback: CallbackQuery, state: FSMContext):
    role = callback.data.split('_')[1]
    await state.update_data(role=role)
    await state.set_state(Register.name)
    await callback.message.edit_text(
        text="Как тебя называть? Напиши имя или псевдоним."
    )
@router.message(Register.name)
async def process_name(message: Message, state: FSMContext):
    data = await state.get_data()
    role = data.get('role')
    await rq.create_user(tg_id=message.from_user.id, role=role, name=message.text)
    await state.clear()
    user = await rq.get_user(message.from_user.id)
    await message.answer(

        text=f"✅ Регистрация завершена! Твоя роль: {role}", reply_markup=reply.main_menu(user.role)
    )