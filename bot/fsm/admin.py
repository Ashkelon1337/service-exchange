from aiogram.fsm.state import State, StatesGroup

class Mailing(StatesGroup): # Рассылка
    waiting_for_message = State()

class UserSearch(StatesGroup):
    waiting_for_id = State()