

# here we create a script that upload texts from you to the database (to populate it with texts)


from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.dispatcher.storage import FSMContext

from keyboards.usual import MenuAdminText
from states.intro_states import UploadTextAdmin
from dispatcher import BotDB
from aiogram import types
from states.intro_states import UploadTextAdmin



async def upload_text_admin_begging(message: types.Message):
    await message.reply("Let's add a new text!")
    await message.answer('Give me the title in chinese please.')
    await UploadTextAdmin.Q1.set()


async def upload_text_admin_add_title(message: types.Message, state: FSMContext):
    title = message.text
    await state.update_data(title=title)
    await message.reply('Give me the title in English please.')
    await UploadTextAdmin.Q2.set()

async def upload_text_admin_add_ENGtitle(message: types.Message, state: FSMContext):
    title = message.text
    await state.update_data(eng_title=title)
    await message.reply('Great! Now give me the text.')
    await UploadTextAdmin.Q3.set()

async def upload_text_admin_add_text(message: types.Message,state: FSMContext):
    text = message.text
    await state.update_data(text=text)
    await message.reply('What is its declared HSK level?')
    await UploadTextAdmin.Q4.set()

async def upload_text_admin_add_HSK(message: types.Message, state: FSMContext):
    hsk = message.text
    await state.update_data(hsk=hsk)
    await message.reply('where did u get it (url)')
    await UploadTextAdmin.Q5.set()


async def upload_text_admin_add_source(message: types.Message, state: FSMContext):

    data = await state.get_data()
    title = data.get('title')
    eng_title = data.get('eng_title')
    text = data.get('text')
    hsk = data.get('hsk')
    url = message.text

    await message.reply('Thank you for your answers')
    try:
        BotDB.text_by_admin(title,text,hsk,url,eng_title)
        await message.answer(f'The text {title} was added to the database', reply_markup=MenuAdminText)
    except Exception as e:
        await message.answer('Ooops, an error')
        await message.answer(e)



def register_handlers_admin_text(dp:Dispatcher):
    dp.register_message_handler(upload_text_admin_begging,commands='Upload_text_admin',state="*")
    dp.register_message_handler(upload_text_admin_add_title, state=UploadTextAdmin.Q1)
    dp.register_message_handler(upload_text_admin_add_ENGtitle, state=UploadTextAdmin.Q2)
    dp.register_message_handler(upload_text_admin_add_text, state=UploadTextAdmin.Q3)
    dp.register_message_handler(upload_text_admin_add_HSK, state=UploadTextAdmin.Q4)
    dp.register_message_handler(upload_text_admin_add_source, state=UploadTextAdmin.Q5)