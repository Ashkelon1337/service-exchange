from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from bot.fsm.admin import Mailing, UserSearch
import database.requests as rq
from bot.keyboards import reply, inline
from bot.keyboards.inline import admin_cancel
from filters.admin import IsAdmin

import asyncio

router = Router()

router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())

async def get_admin_panel():
    users_count = len(await rq.get_users())
    services_count = len(await rq.get_all_services())
    orders_count = len(await rq.get_orders())
    return (
        f"👨‍💼 **Админ-панель**\n\n"
        f"👥 Пользователей: {users_count}\n"
        f"📦 Услуг: {services_count}\n"
        f"📋 Заказов: {orders_count}"
    )

@router.message(Command('admin'))
async def admin_panel(message: Message):
    text = await get_admin_panel()
    await message.answer(text=text, reply_markup=reply.admin_menu)

@router.callback_query(F.data == 'cancel')
async def cancel_handler(callback: CallbackQuery):
    text = await get_admin_panel()
    await callback.message.answer(
        text=text,
        reply_markup=reply.admin_menu
    )
    await callback.answer()

@router.message(F.text == '📊 Статистика')
async def show_stats(message: Message):
    users = await rq.get_users()
    executors = [i for i in users if i.role == 'executor']
    clients = [i for i in users if i.role == 'client']
    orders = await rq.get_orders()
    new_orders = sum(1 for i in orders if i.status == 'new')
    in_progress = sum(1 for o in orders if o.status == 'in_process')
    completed = sum(1 for o in orders if o.status == 'completed')
    cancelled = sum(1 for o in orders if o.status == 'cancelled')
    text =(
        f"📊 **Детальная статистика**\n\n"
        f"👥 Всего пользователей: {len(users)}\n"
        f" 👤 Клиентов: {len(clients)}\n"
        f" 💼 Исполнителей: {len(executors)}\n"
        f"📦 Всего услуг: {len(await rq.get_all_services())}\n"
        f"📋 Всего заказов: {len(await rq.get_orders())}\n"
        f"🆕 Новые: {new_orders}\n"
        f"🔄 В работе: {in_progress}\n"
        f"✅ Выполнено: {completed}\n"
        f"❌ Отменено: {cancelled}"
    )
    await message.answer(text=text)



@router.message(F.text == "📤 Рассылка")
async def start_mailing(message: Message, state: FSMContext):
    await state.set_state(Mailing.waiting_for_message)
    await message.answer(text="📨 Отправь мне сообщение (текст, фото, видео, документ), которое нужно разослать всем пользователям.")

@router.message(Mailing.waiting_for_message)
async def end_mailing(message: Message, state: FSMContext, bot: Bot):
    users = await rq.get_users()
    success = 0
    failed = 0
    status_msg = await message.answer("⏳ Рассылка началась...")
    for user in users:
        try:
            await message.copy_to(chat_id=user.tg_id)
            success += 1
        except Exception:
            failed += 1
        await asyncio.sleep(0.05)
    await status_msg.edit_text(
        f"✅ Рассылка завершена!\n"
        f"📨 Успешно: {success}\n"
        f"❌ Не удалось: {failed}",
        reply_markup=inline.admin_cancel
    )
    await state.clear()

@router.message(F.text == "👥 Пользователи")
async def get_users_menu(message: Message):
    await message.answer(text='Выберите действие:', reply_markup=inline.admin_get_users)

@router.callback_query(F.data == 'find_user')
async def find_user_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text('Введи ID пользователя:')
    await state.set_state(UserSearch.waiting_for_id)
    await callback.answer()

@router.message(UserSearch.waiting_for_id)
async def find_user_by_id(message: Message, state: FSMContext):
    try:
        user_id = int(message.text)
        user = await rq.get_user_by_id(user_id)

        if not user:
            await message.answer("❌ Пользователь не найден", reply_markup=inline.admin_cancel)
        else:
            text = (
                f"👤 **Пользователь #{user.id}**\n"
                f"🆔 Telegram ID: {user.tg_id}\n"
                f"📝 Имя: {user.name}\n"
                f"🎭 Роль: {user.role}\n"
            )
            await message.answer(text=text, reply_markup=inline.admin_cancel)
    except ValueError:
        await message.answer('❌ Введите число!', reply_markup=inline.admin_cancel)
    finally:
        await state.clear()
@router.callback_query(F.data == 'list_users')
async def list_users(callback: CallbackQuery):
    users = await rq.get_users()
    text = '📋 **Все пользователи:**\n\n'
    for user in users:
        text += f"#{user.id} | {user.tg_id} | {user.name} | {user.role}\n"
    await callback.message.edit_text(text=text)
    await callback.answer()
@router.message(F.text == "Услуги")
async def get_services(message: Message):
    services = await rq.get_all_services()
    if not services:
        await message.answer("😢 Пока нет услуг")
        return
    for service in services:
        user = await rq.get_user_by_id(service.user_id)
        text = f'🔹 {service.title}\n💰 {service.price}₽\n👤 {user.name}'
        await message.answer(text=text, reply_markup=inline.detail(service.id))
@router.callback_query(F.data.startswith)
async def delete_service(callback: CallbackQuery):
    service_id = int(callback.data.split('_')[1])
    await rq.delete_service(service_id)
    await callback.message.delete()
    text = await get_admin_panel()
    await callback.message.answer(text=text, reply_markup=reply.admin_menu)