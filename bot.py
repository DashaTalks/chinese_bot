from aiogram import Bot, Dispatcher, types
from dispatcher import BotDB
from aiogram import executor

import logging
from dispatcher import dp


from handlers import user_intro, dict_ch_eng, get_me_texts, getting_text, user_stats
from handlers import upload_text
from handlers import upload_text_admin
from info_btn import about, help_btn

logger = logging.getLogger(__name__)


about.register_handler_about(dp)
help_btn.register_handler_help(dp)
getting_text.register_handlers_getting_text(dp)
user_stats.register_handlers_getting_stats(dp)
user_intro.register_handlers_intro(dp)
upload_text.register_handlers_text(dp)
upload_text_admin.register_handlers_admin_text(dp)
get_me_texts.register_handler_read_text(dp)
dict_ch_eng.register_handlers_dict(dp)



async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()



@dp.message_handler()
async def anythingelse(message: types.Message):
    text = message.text
    id = BotDB.logging_session(user_id=message.from_user.id,action='anythingelse', text_id=0, text=text)
    await message.reply("I'm sorry, I don't know this command. Please choose something from the menu.")











if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_shutdown = shutdown)