from text_analyses.cleaning import  ch_check, eng_check
from aiogram import types
from aiogram.dispatcher.dispatcher import Dispatcher
from dispatcher import BotDB
#import pinyin_jyutping_sentence
from text_analyses.helping_func import PrintWord


def eng_clean(word):
   to = 'to '
   new = to + word
   return new


async def dictionary_eng_ch(message: types.Message):
    text = message.text
    text_ch_check = ch_check(text)
    text_eng_check = eng_check(text)

    dont_know = f"I didn't really got what you said.\n" \
                f" \n  I am a clever cat, but I can translate only chinese to english and back." \
                f"\n I can also suggest you some texts to read that fits your current chinese level." \
                f"\n\nIf you want me to learn something else, write my Mum. She might teach me some new tricks"


    if text_ch_check:
        word = BotDB.ch_to_eng(text)
        texting = PrintWord('usual', message, word)
        await texting.give_meaning()


    elif text_eng_check:
        word = BotDB.eng_to_ch(text)
        if word:
            texting = PrintWord('usual',message, word)
            await texting.give_meaning()


        else:
            new_word = eng_clean(text)
            word = BotDB.eng_to_ch(new_word)
            texting = PrintWord('usual',message, word)
            await texting.give_meaning()






    else:
        await message.answer(dont_know)


def register_handlers_dict(dp:Dispatcher):
    dp.register_message_handler(dictionary_eng_ch)



