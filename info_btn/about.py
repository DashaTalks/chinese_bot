from aiogram import types
from aiogram.dispatcher.dispatcher import Dispatcher
import asyncio

msg_1 = 'Hello! My name is Daria. You can call me Fokla as well'
msg_2 = 'This is me, almost'
msg_3 = 'I have created this bot as my study project. \nI used: Python, MySQL, Aiogram'
msg_4 = 'You can write me here at Telegram. My nick in TG is @Afokl'
msg_5 = 'This bot has 616 texts of different level that covers 8521 of unique words'
msg_6 = 'The main function of these bot is to give you texts according to your language level' \
        '\nYou can read both stories and tweets to enrich your vocabulary in a fun way.'
msg_7 ='In the future I plan to add hindi as one more optional lang as well as some flash cards'
msg_8 ='Stay tuned and have fun!'


async def about_func(message:types.Message):
    await message.answer(msg_1)
    await asyncio.sleep(0.7)
    await message.answer(msg_2)
    await message.answer_photo('https://cdn.pixabay.com/photo/2019/04/13/00/20/dog-4123618__340.jpg')
    await asyncio.sleep(0.7)
    await message.answer(msg_4)
    await asyncio.sleep(0.7)
    await message.answer(msg_3)
    await message.answer(msg_5)
    await message.answer(msg_6)
    await asyncio.sleep(0.7)
    await message.answer(msg_7)
    await message.answer(msg_8)




def register_handler_about(dp:Dispatcher):
    dp.register_message_handler(about_func, commands='About')