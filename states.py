from aiogram.fsm.state import StatesGroup, State

class CreateRoulette(StatesGroup):

    title = State()

    max_users = State()

    winners = State()

    channel = State()
