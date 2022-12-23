# get unique user words
# go through texts and determine how they are different or similar
# display the txt needed
# run the upload text fnc
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram import types
from dispatcher import BotDB
from handlers.upload_text import text_upload
from keyboards.inline import yes_no, hsk_level
from states.intro_states import GetMeText, UploadText
from aiogram.dispatcher.storage import FSMContext
from keyboards.inline_texts import  *

from text_analyses import countings
from text_analyses.countings import counting_words_main


def preparing_texts_for_printing(string,sorted_list):

    string = string[0]

    string = string.replace('[', '')
    string = string.replace(']', '')
    string = string.replace(' ', '')
    string = string.replace("'", '')

    list_of_words_in_text = string.split(',')

    hashing = []


    for char in list_of_words_in_text:
        if char not in sorted_list:
            if char not in hashing:
                hashing.append(char)


    percentage = 100-(round(len(hashing) / len(list_of_words_in_text) * 100))
    return percentage


def percentage_func(percentage, diff, string, hsk, good_texts):
    text_num = string[1]
    text_full = string[2]
    title = string[4]
    title_eng = string[5]

    if percentage < diff:
        combo = []
        combo.append(text_num)
        combo.append(text_full)
        combo.append(hsk)
        combo.append(title)
        combo.append(title_eng)
        combo.append(percentage)
        good_texts.append(combo)

def percentage_func_no_diff(percentage, diff, string, hsk, good_texts):
    text_num = string[1]
    text_full = string[2]
    title = string[4]
    title_eng = string[5]

    combo = []
    combo.append(text_num)
    combo.append(text_full)
    combo.append(hsk)
    combo.append(title)
    combo.append(title_eng)
    combo.append(percentage)
    good_texts.append(combo)


async def choosing_text_to_read(good_texts, user_id, state, message):
    '''
        determine wich keyboard to use while asking the user what he would like to read
    '''
    length = len(good_texts)
    if length > 9:
        keyboards = Text_to_tread_10
    elif length > 8:
        keyboards = Text_to_tread_9
    elif length > 7:
        keyboards = Text_to_tread_8
    elif length > 6:
        keyboards = Text_to_tread_7
    elif length > 5:
        keyboards = Text_to_tread_6
    elif length > 4:
        keyboards = Text_to_tread_5
    elif length > 3:
        keyboards = Text_to_tread_4
    elif length > 2:
        keyboards = Text_to_tread_3
    elif length > 1:
        keyboards = Text_to_tread_2
    else:
        keyboards = Text_to_tread_1

    await state.update_data(good_texts=good_texts)
    await state.update_data(userId=user_id)

    await message.answer('What text would you like to read?', reply_markup=keyboards)
    await GetMeText.Q2.set()


async def printing_texts(good_texts, message):

    '''
    print texts that user can read
    '''

    counter = 1

    for i in good_texts:
        number = i[0]
        hsk = i[2]
        title = i[3]
        title_eng = i[4]
        per = i[5]
        string = f'{counter}. title:"{title}", title eng: "{title_eng}" (hsk{hsk}). You know {100 - per}% ' \
                 f'of this text'
        await message.answer(string)
        counter = counter + 1

        if counter == 11:
            break


async def get_me_the_text_intro(message: types.Message, state: FSMContext):
    '''
        get a usual message as a param and launch the process of getting texts to read for a user
    '''

    user_id = message.from_user.id
    user_unique_words = BotDB.get_unique_words(user_id)
    clean_list = []
    for i in user_unique_words:
        clean_list.append(i)
    clean_list = sorted(clean_list, key=lambda x: x[1])
    sorted_list = []
    for i in clean_list:
        sorted_list.append(i[0])
    await state.update_data(sorted_list_user_words=sorted_list)
    await GetMeText.Q1.set()
    await message.answer('how difficult the text should be? Give me the % of new words. (Only number, no %)')


async def get_me_the_text_intro_cb(callback: types.CallbackQuery, state:FSMContext):
    '''
    get a callback as a param and launch the process of getting texts to read for a user
    '''
    user_id = callback.from_user['id']
    user_unique_words = BotDB.get_unique_words(user_id)
    clean_list = []
    for i in user_unique_words:
        clean_list.append(i)
    clean_list = sorted(clean_list, key=lambda x: x[1])
    sorted_list = []
    for i in clean_list:
        sorted_list.append(i[0])
    await state.update_data(sorted_list_user_words=sorted_list)
    await GetMeText.Q1.set()
    await callback.message.answer('how difficult the text should be? Give me the % of new words. (Only number, no %)')


async def get_me_texts_anal(message: types.Message, state: FSMContext):
    '''
    it gets all the texts from DB that the user haven't read, analyses them
    and return the one that fits the requirements
    '''
    user_id = message.from_user.id
    diff = int(message.text)
    data = await state.get_data()
    sorted_list = data.get('sorted_list_user_words')

    list_of_texts = BotDB.get_all_texts_for_a_user(user_id)
    await state.update_data(list_of_texts=list_of_texts)
    await state.update_data(diff=diff)

    good_texts = []
    counter = 0

    for string in list_of_texts:
        hsk = string[3]


        percent = preparing_texts_for_printing(string, sorted_list)
        percentage_func(percent, diff, string, hsk, good_texts)


        if len(good_texts) > 9:
            break

    updates = []

    if len(good_texts) < 10:

        if len(BotDB.get_unique_words(user_id)) < 100:
            await message.answer('There is less than 100 words in your vocabulary. So we can not'
                                 ' suggest you are text based on your vocabulary')
            await message.answer('Choose an HSK level, so we can give you an appropriate text.', reply_markup=hsk_level)

            await state.update_data(good_texts=good_texts)

            await GetMeText.Q3.set()

        else:
            for string in list_of_texts:

                hsk = string[3]

                percent = preparing_texts_for_printing(string, sorted_list)
                print('percent:',percent)

                percentage_func_no_diff(percent, diff, string, hsk, updates)


                updates = sorted(updates, key=lambda x: x[5])

                for i in updates:
                    if i not in good_texts:
                        good_texts.append(i)
                    if len(good_texts) > 9:
                        break
            await state.update_data(good_texts=good_texts)
            await printing_texts(good_texts, message)
            await choosing_text_to_read(good_texts, user_id, state, message)
            await state.update_data(good_texts=good_texts)


    else:
        await printing_texts(good_texts, message)
        await choosing_text_to_read(good_texts, user_id, state, message)
        await state.update_data(good_texts=good_texts)


async def got_hsk(callback: types.CallbackQuery, state:FSMContext):
    """
    Whe you choose an HSK and got based on it
    """

    hsk_user = int(callback.data[3])
    user_id = callback.from_user['id']
    data = await state.get_data()
    diff = data.get('diff')
    list_of_texts = data.get('list_of_texts')
    good_texts = data.get('good_texts')

    for string in list_of_texts:

        hsk = string[3]

        if int(hsk) != int(hsk_user):
            continue
        updates = []
        percent = 0

        percentage_func(percent, diff, string, hsk, updates)

        updates = sorted(updates, key=lambda x: x[5])

        for i in updates:
            if i not in good_texts:
                good_texts.append(i)
            if len(good_texts) > 9:
                break

    await printing_texts(good_texts, callback.message)

    await callback.answer()
    await choosing_text_to_read(good_texts, user_id, state, callback.message)


async def btn(callback: types.CallbackQuery, state: FSMContext):
    """
    get info from the btn (one-to-ten) and return the text acordingly
    """
    await callback.answer()
    number = int(callback.data)-1
    data = await state.get_data()
    good_texts = data.get('good_texts')
    user_id = callback.from_user['id']
    text = good_texts[number]
    text_id = int(text[0])
    await callback.message.answer(text)

    all_words, unique, whole_text = counting_words_main(text[1])

    await callback.message.answer('Great! I\'ve got your text')

    await callback.message.answer(whole_text)
    await callback.message.answer('Do you understand all words in the text?', reply_markup=yes_no)
    await UploadText.Q2.set()

    new_words_displayed = []
    old_words_displayed = []

    await state.update_data(all_words=all_words)
    await state.update_data(unique=unique)
    await state.update_data(whole_text=whole_text)
    await state.update_data(new_words_displayed=new_words_displayed)
    await state.update_data(old_words_displayed=old_words_displayed)
    await state.update_data(text_id=text_id)


def register_handlers_getting_text(dp:Dispatcher):
    dp.register_message_handler(get_me_the_text_intro, commands=["Read_a_text"], state="*")
    dp.register_callback_query_handler(get_me_the_text_intro_cb, text='read_text', state="*")
    dp.register_message_handler(get_me_texts_anal, state=GetMeText.Q1)
    dp.register_callback_query_handler(btn, state=GetMeText.Q2, text='1')
    dp.register_callback_query_handler(btn, state=GetMeText.Q2, text='2')
    dp.register_callback_query_handler(btn, state=GetMeText.Q2, text='3')
    dp.register_callback_query_handler(btn, state=GetMeText.Q2, text='4')
    dp.register_callback_query_handler(btn, state=GetMeText.Q2, text='5')
    dp.register_callback_query_handler(btn, state=GetMeText.Q2, text='6')
    dp.register_callback_query_handler(btn, state=GetMeText.Q2, text='7')
    dp.register_callback_query_handler(btn, state=GetMeText.Q2, text='8')
    dp.register_callback_query_handler(btn, state=GetMeText.Q2, text='9')
    dp.register_callback_query_handler(btn, state=GetMeText.Q2, text='10')
    dp.register_callback_query_handler(got_hsk, state=GetMeText.Q3, text='HSK1')
    dp.register_callback_query_handler(got_hsk, state=GetMeText.Q3, text='HSK2')
    dp.register_callback_query_handler(got_hsk, state=GetMeText.Q3, text='HSK3')
    dp.register_callback_query_handler(got_hsk, state=GetMeText.Q3, text='HSK4')
    dp.register_callback_query_handler(got_hsk, state=GetMeText.Q3, text='HSK5')
    dp.register_callback_query_handler(got_hsk, state=GetMeText.Q3, text='HSK6')