from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def client_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Каталог услуг")],
            [KeyboardButton(text="📦 Мои заказы")],
        ], resize_keyboard=True, is_persistent=True
    )
def executor_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Каталог услуг")],
            [KeyboardButton(text="➕ Создать услугу")],
            [KeyboardButton(text="📦 Мои заказы")],
        ], resize_keyboard=True, is_persistent=True
    )
def main_menu(role):
    if role == 'executor':
        return executor_menu()
    return client_menu()

admin_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="📊 Статистика")],
    [KeyboardButton(text="📤 Рассылка")],
    [KeyboardButton(text="👥 Пользователи")],
    [KeyboardButton(text="Услуги")]
], resize_keyboard=True, is_persistent=True)
