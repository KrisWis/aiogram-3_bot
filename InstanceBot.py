from aiogram import Dispatcher, Router, Bot
from aiogram.fsm.storage.memory import MemoryStorage
from Config import BOT_TOKEN
from aiogram.fsm.state import State, StatesGroup

storage = MemoryStorage()

bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher()
router = Router()
dp.include_router(router)

class UserStates(StatesGroup):
    test = State()