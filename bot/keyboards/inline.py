from mimetypes import inited

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_message = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='👤 Клиент', callback_data='role_client')],
    [InlineKeyboardButton(text='💼 Исполнитель', callback_data='role_executor')]
])
def detail(service_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🔍 Подробнее', callback_data=f'detail_{service_id}')],
    ])
def order(service_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Заказать', callback_data=f'order_{service_id}')],
        [InlineKeyboardButton(text='Назад', callback_data='Back')],
    ])
def cancel_order_client(order_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='❌ Отменить', callback_data=f'cancel_{order_id}')]
    ])

def order_executor_new(order_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='✅ Взять в работу', callback_data=f'take_{order_id}')],
        [InlineKeyboardButton(text='❌ Отклонить', callback_data=f'cancel_{order_id}')]
    ])

def order_executor_in_process(order_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='✅ Выполнено', callback_data=f'complete_{order_id}')],
        [InlineKeyboardButton(text='❌ Отклонить', callback_data=f'cancel_{order_id}')]
    ])
admin_get_users = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🔍 Найти по ID", callback_data="find_user")],
    [InlineKeyboardButton(text="📋 Список всех", callback_data="list_users")]
])
admin_cancel = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='cancel')]
])
def delete_service(service_id):
    return InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Удалить', callback_data=f'delete_{service_id}')]
])

show_orders = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Показать новые заказы', callback_data='show_new')],
    [InlineKeyboardButton(text='Показать заказы в процессе', callback_data="show_in_process")],
    [InlineKeyboardButton(text='Показать отклонённые', callback_data='show_cancelled')],
    [InlineKeyboardButton(text='Показать выполненные задачи', callback_data='show_completed')],
])