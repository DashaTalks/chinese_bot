import logging
from aiogram import Bot, Dispatcher
from extra import db
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import load_config

config = load_config()

# Configure logging
logging.basicConfig(level=logging.INFO)

# prerequisites
if not config.tg_bot.token:
    exit("No token provided")

# init
storage = MemoryStorage()
bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
dp = Dispatcher(bot, storage=storage)
BotDB = db.BotDB()

