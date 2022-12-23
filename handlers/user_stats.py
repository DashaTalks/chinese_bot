#user can see how many words
# how many texts
# how many days used

from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram import types
from dispatcher import BotDB
from aiogram.dispatcher.storage import FSMContext

async def give_me_my_stats(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_unique_words = BotDB.get_unique_words(user_id)
    if user_unique_words:
        await message.answer(user_unique_words)
    else:
        await message.answer('There is no words in your vocabulary list. \nPlease read some text, so we '
                             'can add new words')


def register_handlers_getting_stats(dp:Dispatcher):
    dp.register_message_handler(give_me_my_stats, commands=['My_stats'], state='*')