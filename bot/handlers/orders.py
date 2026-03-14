from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

import database.requests as rq
from utils import order_display

router = Router()

@router.message(F.text == '📦 Мои заказы')
async def show_my_orders(message: Message):
    user = await rq.get_user(message.from_user.id)
    if user.role == 'client':
        orders = await rq.get_client_orders(user.id)
        await order_display.show_client_orders(message, orders)
    else:
        orders = await rq.get_executor_orders(user.id)
        await order_display.show_executor_orders(message, orders)

@router.callback_query(F.data.startswith('cancel_'))
async def cancel_order(callback: CallbackQuery):
    order_id = int(callback.data.split('_')[1])
    order = await rq.get_order(order_id)
    service = await rq.get_service(order.service_id)
    await rq.update_order_status(order_id, 'cancelled')
    cancelled_user = await rq.get_user(callback.from_user.id)
    if cancelled_user.id == order.client_id: # Отменил клиент
        user = await rq.get_user_by_id(order.executor_id)
        await callback.bot.send_message(

            chat_id=user.tg_id,
            text=f"❌ Клиент отменил заказ #{order_id} на '{service.title}'"
        )
        await callback.message.edit_text(
            text=callback.message.text + "\n\n❌ Вы отменили заказ"
        )
    else:
        user = await rq.get_user_by_id(order.client_id)
        await callback.bot.send_message(
            chat_id=user.tg_id,
            text=f"❌ Исполнитель отменил заказ #{order_id} на '{service.title}'"
        )
        await callback.message.edit_text(text=callback.message.text + "\n\n❌ Исполнитель отменил заказ")
    await callback.answer("✅ Заказ отменён")