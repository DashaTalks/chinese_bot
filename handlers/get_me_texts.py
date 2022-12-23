from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.dispatcher.storage import FSMContext
from aiogram import types
from dispatcher import BotDB
from keyboards.usual import mainMenu
from states.intro_states import UploadText, IntroQuestions


async def get_me_text(message: types.Message):
    text = BotDB.get_rand_text()
    await message.answer(text)


def register_handler_read_text(dp:Dispatcher):
    dp.register_message_handler(get_me_text, commands='read_texts')