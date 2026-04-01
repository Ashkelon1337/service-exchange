from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from bot.keyboards.inline import show_orders
import database.requests as rq
from utils import order_display

router = Router()

@router.message(F.text == '📦 Мои заказы')
async def show_my_orders(message: Message):
    user = await rq.get_user(message.from_user.id)
    orders = await rq.get_user_order(user.id)
    new_orders = []
    in_process = []
    complete_orders = []
    canceled = []
    if not orders:
        await message.answer(text='У вас нет заказов')
        return
    for order in orders:
        if order.status == 'new':
            new_orders.append(order)
        elif order.status == 'in_process':
            in_process.append(order)
        elif order.status == 'cancelled':
            canceled.append(order)
        elif order.status == 'completed':
            complete_orders.append(order)
    text = f'Заказов всего - {len(orders)}\n{len(new_orders)} Новых\n{len(in_process)} В процессе\n{len(canceled)} Отклоненных\n{len(complete_orders)} Выполненных'
    await message.answer(text=text, reply_markup=show_orders)

@router.callback_query(F.data.startswith('show_'))
async def show_new_orders(callback: CallbackQuery):
    status = callback.data.split('_')[1:]
    status = ''.join(status)
    print(status)
    user = await rq.get_user(callback.from_user.id)
    orders = await rq.get_orders_by_status(status=status, user_id=user.id)
    if user.role == 'executor':
        await order_display.show_executor_orders(message=callback.message, orders=orders)
    else:
        await order_display.show_client_orders(message=callback.message, orders=orders)

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