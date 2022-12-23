from aiogram import types
from aiogram.dispatcher.dispatcher import Dispatcher

from keyboards.usual import helpMarkup


async def help_func(message:types.Message):
    await message.answer('Hello! How can I help you?', reply_markup=helpMarkup)


def register_handler_help(dp:Dispatcher):
    dp.register_message_handler(help_func, commands='Help')