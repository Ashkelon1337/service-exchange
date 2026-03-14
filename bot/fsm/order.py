from aiogram.fsm.state import State, StatesGroup

class Order(StatesGroup):
    comment = State()
