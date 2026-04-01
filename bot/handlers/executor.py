from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
import database.requests as rq
from aiogram.fsm.context import FSMContext
from bot.fsm.create_service import CreateService
from bot.keyboards import reply
router = Router()

@router.callback_query(F.data.startswith('take_'))
async def take_order_handler(callback: CallbackQuery):
    await callback.answer()
    order_id = int(callback.data.split('_')[1])
    order = await rq.get_order(order_id)
    service = await rq.get_service(order.service_id)
    user = await rq.get_user_by_id(order.client_id)
    await rq.update_order_status(order_id, 'in_process')
    await callback.bot.send_message(chat_id=user.tg_id,
                                    text=f"✅ Исполнитель взял в работу заказ #{order_id} на '{service.title}'")
    await callback.message.edit_text(
        text=callback.message.text + "\n\n✅ Вы взяли заказ в работу",
        reply_markup=None
    )
    await callback.answer("✅ Заказ принят в работу")

@router.callback_query(F.data.startswith('complete_'))
async def complete_order_handler(callback: CallbackQuery):
    order_id = int(callback.data.split('_')[1])
    order = await rq.get_order(order_id)
    service = await rq.get_service(order.service_id)
    client = await rq.get_user_by_id(order.client_id)
    await rq.update_order_status(order_id, 'completed')
    await callback.bot.send_message(chat_id=client.tg_id,
                                    text=f"🎉 Заказ #{order_id} на '{service.title}' выполнен!"
                                    )
    await callback.message.edit_text(text=callback.message.text + '\n\n✅ Заказ выполнен', reply_markup=None)
    await callback.answer("✅ Заказ отмечен как выполненный")


@router.message(F.text == '➕ Создать услугу')
async def create_service_start(message: Message, state: FSMContext):
    await state.set_state(CreateService.title)
    await message.answer("Введи название услуги:")

@router.message(CreateService.title)
async def create_service_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(CreateService.description)
    await message.answer("Опиши услугу подробно:")
@router.message(CreateService.description)
async def create_service_description(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(CreateService.price)
    await message.answer("Укажи цену (только цифры):")
@router.message(CreateService.price)
async def create_service_end(message: Message, state: FSMContext):
    try:
        price = int(message.text)
        data = await state.get_data()
        user = await rq.get_user(message.from_user.id)

        await rq.create_service(
            user_id=user.id,
            title=data['title'],
            description=data['description'],
            price=price
        )
        await state.clear()
        await message.answer("✅ Услуга создана!",
            reply_markup=reply.main_menu("executor"))
    except ValueError:
        await message.answer("❌ Цена должна быть числом. Попробуй ещё раз")
