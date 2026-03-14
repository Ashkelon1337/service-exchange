from aiogram.fsm.state import State, StatesGroup
class CreateService(StatesGroup):
    title = State()
    description = State()
    price = State()