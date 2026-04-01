from aiogram.types import Message
from bot.keyboards import inline
import database.requests as rq

async def show_client_orders(message: Message, orders):
    if not orders:
        await message.answer("📭 У тебя пока нет заказов")
        return

    for order in orders:
        service = await rq.get_service(order.service_id)
        user = await rq.get_user_by_id(order.executor_id)
        text = f"📦 Заказ #{order.id}\n"
        text += f"📌 Услуга: {service.title}\n"
        text += f"👤 Исполнитель: {user.name}\n"
        text += f"📊 Статус: {order.status}\n"
        keyboard = inline.cancel_order_client(order.id)
        await message.answer(text=text, reply_markup=keyboard)


async def show_executor_orders(message: Message, orders):
    if not orders:
        await message.answer("📭 Заказов на твои услуги пока нет")
        return

    for order in orders:
        service = await rq.get_service(order.service_id)
        user = await rq.get_user_by_id(order.client_id)
        text = f"📦 Заказ #{order.id}\n"
        text += f"📌 Услуга: {service.title}\n"
        text += f"👤 Клиент: {user.name}\n"
        text += f"📊 Статус: {order.status}\n"
        text += f"📝 Комментарий: {order.comment}\n"
        if order.status == 'new':
            kb = inline.order_executor_new(order.id)
        elif order.status == 'in_process':
            kb = inline.order_executor_in_process(order.id)
        else:
            kb = None
        await message.answer(text=text, reply_markup=kb)