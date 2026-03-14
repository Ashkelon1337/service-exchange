from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from pyexpat.errors import messages

import database.requests as rq
import bot.keyboards.inline as inline
from aiogram.fsm.context import FSMContext
from bot.fsm.order import Order

router = Router()

@router.message(F.text == '📋 Каталог услуг')
async def Catalog(message: Message):
    services = await rq.get_all_services()
    if not services:
        await message.answer("😢 Пока нет услуг")
        return
    for service in services:
        user = await rq.get_user_by_id(service.user_id)
        text = f'🔹 {service.title}\n💰 {service.price}₽\n👤 {user.name}'
        await message.answer(text=text, reply_markup=inline.detail(service.id))
@router.callback_query(F.data.startswith('detail_'))
async def get_detail(callback: CallbackQuery):
    await callback.answer()
    service_id = int(callback.data.split('_')[1])
    service = await rq.get_service(service_id)
    await callback.message.answer(service.description, reply_markup=inline.order(service_id))
@router.callback_query(F.data.startswith('order_'))
async def start_order(callback: CallbackQuery, state: FSMContext):
    service_id = int(callback.data.split('_')[1])
    await state.update_data(service_id=service_id)
    await state.set_state(Order.comment)
    await callback.message.answer("Напишите комментарий к заказу:")
@router.message(Order.comment)
async def process_comment(message: Message, state: FSMContext):
    data = await state.get_data()
    service_id = data.get('service_id')
    service = await rq.get_service(service_id)
    client = await rq.get_user(message.from_user.id)
    safe_comment = message.text or 'Без комментария'

    order_id = await rq.create_order(
        client_id=client.id,
        executor_id=service.user_id,
        service_id=service_id,
        comment=safe_comment
    )

    executor = await rq.get_user_by_id(service.user_id)

    await message.bot.send_message(
        chat_id=executor.tg_id,
        text=f"🔔 Новый заказ #{order_id}!\n"
             f"📌 Услуга: {service.title}\n"
             f"👤 Клиент: {client.name}\n"
             f"📝 Комментарий: {message.text}"
    )


    await state.clear()
    await message.answer('Успешно')

