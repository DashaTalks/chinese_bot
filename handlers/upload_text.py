
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.dispatcher.storage import FSMContext
from dispatcher import BotDB
from aiogram import types

from keyboards.inline import yes_no, words_understanding, yes_no_translation, yes_no_more
from keyboards.usual import mainMenu
from text_analyses.countings import counting_words_main
from states.intro_states import UploadText
import asyncio

# you need to add so at least to cheack if at leasr one chinesse character there
#logging mistaken words

from text_analyses.users_words_database import adding_all_words_to_db, adding_unique_words_to_db


async def start_uploading(message: types.Message):
        """
        Func that asks for the text and set the FSM. Sets Q1
        """
        await message.reply('Oh, that is something I\'m always happy to do!')
        await message.answer('Send me your text please.')
        await UploadText.Q1.set()


async def text_upload(message: types.Message, state: FSMContext):
        """
        Sets Q2
        Func that get the text from the user and asks if the user knows all words.
        It uses inline buttons
        Sets next FSM
        Add to sata storage: user id, all unique words from the texts, all words from the text and the whole text
        """

        text = message.text
        user_id = message.from_user.id

        all_words, unique, whole_text = counting_words_main(text)

        await message.reply('Great! I\'ve got your text')

        await message.answer(whole_text)
        await message.answer('Do you understand all words in the text?', reply_markup=yes_no)
        await UploadText.Q2.set()

        new_words_displayed = []
        old_words_displayed = []

        await state.update_data(all_words=all_words)
        await state.update_data(unique=unique)
        await state.update_data(whole_text=whole_text)
        await state.update_data(user_id=user_id)
        await state.update_data(new_words_displayed=new_words_displayed)
        await state.update_data(old_words_displayed=old_words_displayed)


async def text_understanding_yes(callback: types.CallbackQuery, state: FSMContext):
        """
        Sets Q6
        it is a call back catcher. It takes yes as an answer and upload all the words as - known
        """
        await callback.message.answer(f"Okay, if text is long, it might take a while")
        await callback.message.edit_reply_markup()


        #Get all data from the memory
        data = await state.get_data()
        text = data.get('whole_text')
        unique = data.get('unique')
        words = data.get('all_words')
        text_id_db = data.get('text_id')
        user = int(callback.from_user['id'])

        #Upload text to the DB
        text_id = BotDB.add_text(text)
        log_id = BotDB.logging_session(user, 'UploadText', text_id[1], text)
        BotDB.user_text(log_id[1], text_id[1])

        old_number = len(BotDB.get_unique_words(user))

        adding_all_words_to_db(words, text_id)
        adding_unique_words_to_db(unique, user, 'Know')

        if text_id_db:
            BotDB.text_status_update_two(user,text_id_db)

        number = len(BotDB.get_unique_words(user))
        await callback.message.answer(f'Congratulation! You know {number} unique words! ')
        await callback.message.answer(f'This is {number - old_number} new words!')
        await callback.answer()
        await callback.message.answer(f'Do you want to continue?',
                                      reply_markup=yes_no_more)
        await UploadText.Q6.set()


async def text_understanding_no(callback: types.CallbackQuery, state: FSMContext):
        """
          Sets Q3
          This func clean up the text (delete all not relevant characters) then it split texts into words
          Func creates two lists of words sorted by the frequency of use:
          One for words user knows and another for words user don't know.
          All that data is uploaded to the storage (sorted_list_new_words,
          initial_clean_new_list, sorted_list_known_words"""
        data = await state.get_data()
        unique = data.get('unique')
        user = callback.from_user['id']

        new_for_user = []
        known_by_user = []
        to_clean_up = []

        for word in unique:
            result = BotDB.word_is_known_by_user(word, user)
            combo = []
            if result[0][0] is not None:

                try:
                    combo.append(word)
                    combo.append(result[0][1])
                    combo.append(result[0][2])
                    combo.append(result[0][3])
                    known_by_user.append(combo)
                except:
                    print('issues with', word)

            else:
                freq = BotDB.get_unknown_freq(word)
                combo.append(word)

                try:
                    combo.append(freq[0][0])
                    combo.append(freq[0][1])
                except Exception as e:
                    to_clean_up.append(word)
                    #I also need to log it in

                new_for_user.append(combo)

        if to_clean_up:
            for i in to_clean_up:
                for el in new_for_user:
                    if el[0] == i:
                        new_for_user.remove(el)



        sorted_list_new_words = sorted(new_for_user, key=lambda x: x[1])
        sorted_list_known_words = sorted(known_by_user, key=lambda x: (x[2], x[1]))


        await state.update_data(sorted_list_new_words=sorted_list_new_words)
        await state.update_data(initial_clean_new_list=sorted_list_new_words)
        await state.update_data(sorted_list_known_words=sorted_list_known_words)
        await callback.message.edit_reply_markup()
        await asyncio.sleep(0.7)

        await callback.message.answer('Now we will start the process of determining '
                                      'what words you don\'t know. \n\nKnowing the words '
                             'that you know allow me to accurately suggest you texts.'
                             '\n\nPlease mark all the words you don\'t know and finish the process')
        await callback.message.answer(f'Do you want to type words, that you do not know?'
                                      f' or I can give you translation of all new words '
                                      f'for you based on frequency?', reply_markup=yes_no_translation)
        await callback.answer()
        await UploadText.Q3.set()


async def give_me_translation(callback: types.CallbackQuery, state: FSMContext):
        """
        Set Q4
        Print the translation for all words (new and old)
        """
        data = await state.get_data()
        sorted_list_known_words = data.get('sorted_list_known_words')
        sorted_list_new_words = data.get('sorted_list_new_words')
        old_words_displayed = data.get('old_words_displayed')
        new_words_displayed = data.get('new_words_displayed')

        remove_list_words = []
        await state.update_data(remove_list_words=remove_list_words)
        await callback.message.edit_reply_markup()

        to_remove = []

        counter = 0
        number_to_display = 1

        await callback.message.answer('Those are top words by difficulty that are not yet in your vocabulary:')
        while number_to_display < 6:
            try:
                word = BotDB.ch_to_eng(sorted_list_new_words[counter][0])
                if word:
                    n = 0
                    word_lst = []
                    while n < len(word):
                        word_lst.append(word[n][0])
                        n = n + 1
                    word_lst = '; '.join(word_lst).split(',')

                    # translate = PrintWord('inline', callback, word)
                    await callback.message.answer(
                        f'{number_to_display}.{sorted_list_new_words[counter][0]} {sorted_list_new_words[counter][2]} - {word_lst[0]}')
                    # await translate.give_meaning()
                    number_to_display = number_to_display + 1

                    new_words_displayed.append(word_lst[0])

                else:
                    # you need to try to get eng translation from shorter dict
                    to_remove.append(sorted_list_new_words[counter])

                counter = counter + 1
            except:
                number_to_display = 6

        if counter < 5:
            await callback.message.answer('No more new words')

        for i in to_remove:
            sorted_list_new_words.remove(i)
        await state.update_data(sorted_list_new_words=sorted_list_new_words)

        counter_2 = 0
        number_to_display_new = counter + 1

        if sorted_list_known_words:
            await callback.message.answer('The top words that are already in your vocabulary.'
                                          ' Those that you met the least often')
            while number_to_display_new < 4 + number_to_display:
                try:
                    word = BotDB.ch_to_eng(sorted_list_known_words[counter_2][0])
                    if word:
                        n = 0
                        word_lst = []
                        while n < len(word):
                            word_lst.append(word[n][0])
                            n = n + 1
                        word_lst = '; '.join(word_lst).split(',')

                        await callback.message.answer(
                            f'{number_to_display_new}. {sorted_list_known_words[counter_2][0]} '
                            f'{sorted_list_known_words[counter_2][3]} - {word_lst[0]}')
                        number_to_display_new = number_to_display_new + 1

                        old_words_displayed.append(word_lst[0])
                    else:
                        print(sorted_list_known_words[counter_2][0])
                    counter_2 = counter_2 + 1
                except:

                    number_to_display_new = 4 + number_to_display

        if counter_2 < 3:
            await callback.message.answer('No more old words to display')

        await state.update_data(old_words_displayed=old_words_displayed)
        await state.update_data(new_words_displayed=new_words_displayed)
        await state.update_data(just_displayed_n=counter)
        await state.update_data(just_displayed_o=counter_2)

        await callback.message.answer(
                'Do you know all those words? Choose the one you do not know. (Click on the numbers of words you don\'t'
                'know. Then finish the process)'
                '\n\nwe will mark them as "learning" and exclude from your base vocabulary'
                ' for now. ', reply_markup=words_understanding)

        await UploadText.Q4.set()
        await callback.answer()


async def btn(callback: types.CallbackQuery, state: FSMContext):
    '''
    No new state.
    BTN - learning words
    '''
    data = await state.get_data()
    sorted_list_known_words = data.get('sorted_list_known_words')
    sorted_list_new_words = data.get('sorted_list_new_words')
    remove_list_words = data.get('remove_list_words')
    old_words_displayed = data.get('old_words_displayed')
    new_words_displayed = data.get('new_words_displayed')
    just_displayed_n = data.get('just_displayed_n')
    just_displayed_o = data.get('just_displayed_o')

    #sorted_list_new_words = sorted_list_new_words[new_start_n:]

    new_start_o = len(old_words_displayed)-just_displayed_o
    sorted_list_known_words = sorted_list_known_words[new_start_o:]

    await callback.answer()
    number = callback.data
    btn_int = int(number)-1

    if btn_int > 4:
        list_used = sorted_list_known_words
        btn_int = btn_int - 5
    else:
        list_used = sorted_list_new_words

    await callback.message.answer(f'Word {list_used[btn_int][0]} will have a status '
                                  f'"Learning" after you finish the process')
    remove_list_words.append(list_used[btn_int][0])

    await state.update_data(sorted_list_new_words=sorted_list_new_words)
    await state.update_data(remove_list_words=remove_list_words)


async def finishing(callback: types.CallbackQuery, state: FSMContext):
    '''
    Set Q6 state
    The process is finishing - add new words to the database (old, new)
    Plus print everything
    '''

    data = await state.get_data()
    sorted_list_known_words = data.get('sorted_list_known_words')
    sorted_list_new_words = data.get('sorted_list_new_words')
    remove_list_words = data.get('remove_list_words')
    initial_clean_new_list = data.get('initial_clean_new_list')

    if remove_list_words:
        for word in remove_list_words:
            for cell in initial_clean_new_list:
                if cell[0] == word:
                    initial_clean_new_list.remove(cell)
            for cell in sorted_list_new_words:
                if cell[0] == word:
                    sorted_list_new_words.remove(cell)

    to_add_to_db = []

    for i in initial_clean_new_list:
        to_add_to_db.append(i[0])
    for i in sorted_list_new_words:
        to_add_to_db.append(i[0])

    text = data.get('whole_text')
    user = callback.from_user['id']
    words = data.get('all_words')

    old_number = len(BotDB.get_unique_words(user))

    for i in remove_list_words:
        words.remove(i)

    text_id = BotDB.add_text(text)
    log_id = BotDB.logging_session(user, 'UploadText_learning_words', text_id[1], text)
    BotDB.user_text(log_id[1], text_id[1])


    adding_all_words_to_db(words, text_id)
    adding_unique_words_to_db(to_add_to_db, user,'Know')
    adding_unique_words_to_db(remove_list_words, user, 'learning')
    text_id_db = data.get('text_id')

    BotDB.text_status_update(user, text_id_db, 'read')

    number = len(BotDB.get_unique_words(user))
    await callback.message.answer(f'Congratulation! You know {number} unique words! ')
    await callback.message.answer(f'This is {number-old_number} new words!')
    if to_add_to_db:
        await callback.message.answer(f'new unique words:{to_add_to_db}')
    else:
        await callback.message.answer(f'No new unique words were added')

    if remove_list_words:
        await callback.message.answer(f'words added as learning:{remove_list_words}')
    else:
        await callback.message.answer(f'No new learning words were added')

    await callback.message.answer(f'Do you want to upload some more texts?', reply_markup=yes_no_more)
    await UploadText.Q6.set()



async def display_more_words(callback: types.CallbackQuery, state: FSMContext):
    '''Set Q5'''
    data = await state.get_data()
    sorted_list_known_words = data.get('sorted_list_known_words')
    sorted_list_new_words = data.get('sorted_list_new_words')
    old_words_displayed = data.get('old_words_displayed')
    new_words_displayed = data.get('new_words_displayed')


    new_start_n = len(new_words_displayed)
    sorted_list_new_words = sorted_list_new_words[new_start_n:]

    new_start_o = len(old_words_displayed)
    sorted_list_known_words = sorted_list_known_words[new_start_o:]

    to_remove = []

    counter = 0
    number_to_display = 1
    counter_2 = 0

    if len(sorted_list_known_words) > 0 or len(sorted_list_new_words)>0:

        await callback.message.answer('Those are top words by difficulty that are not yet in your vocabulary:')

        while number_to_display < 6:
            try:
                word = BotDB.ch_to_eng(sorted_list_new_words[counter][0])
                if word:
                    n = 0
                    word_lst = []
                    while n < len(word):
                        word_lst.append(word[n][0])
                        n = n + 1
                    word_lst = '; '.join(word_lst).split(',')

                    # translate = PrintWord('inline', callback, word)
                    await callback.message.answer(
                        f'{number_to_display}.{sorted_list_new_words[counter][0]} {sorted_list_new_words[counter][2]} - {word_lst[0]}')
                    # await translate.give_meaning()
                    number_to_display = number_to_display + 1

                    new_words_displayed.append(word_lst[0])

                else:
                    # you need to try to get eng translation from shorter dict
                    to_remove.append(sorted_list_new_words[counter])

                counter = counter + 1
            except:
                number_to_display = 6

        if counter < 5:
            await callback.message.answer('No more new words')

        for i in to_remove:
            sorted_list_new_words.remove(i)
        await state.update_data(sorted_list_new_words=sorted_list_new_words)


        number_to_display_new = counter + 1

        if sorted_list_known_words:
            await callback.message.answer('The top words that are already in your vocabulary.'
                                          ' Those that you met the least often')
            while number_to_display_new < 4 + number_to_display:
                try:
                    word = BotDB.ch_to_eng(sorted_list_known_words[counter_2][0])
                    if word:
                        n = 0
                        word_lst = []
                        while n < len(word):
                            word_lst.append(word[n][0])
                            n = n + 1
                        word_lst = '; '.join(word_lst).split(',')

                        await callback.message.answer(
                            f'{number_to_display_new}. {sorted_list_known_words[counter_2][0]} '
                            f'{sorted_list_known_words[counter_2][3]} - {word_lst[0]}')
                        number_to_display_new = number_to_display_new + 1

                        old_words_displayed.append(word_lst[0])

                    else:
                        pass
                    counter_2 = counter_2 + 1
                except:
                    number_to_display_new = 4 + number_to_display

        if counter_2 < 3:
            await callback.message.answer('No more old words to display')

        await callback.message.answer('Next step:', reply_markup=words_understanding)

    else:
        await callback.message.answer('Sorry, no more words left. Everything was added to your library')
        await callback.message.answer('Finish the process')
        await UploadText.Q5.set()
        await finishing(callback, state)

    await state.update_data(old_words_displayed=old_words_displayed)
    await state.update_data(new_words_displayed=new_words_displayed)
    await state.update_data(just_displayed_n=counter)
    await state.update_data(just_displayed_o=counter_2)


async def final_part_out(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(f'We have finished here')
    await callback.message.answer(f'What do you want to do next?', reply_markup=mainMenu)
    await callback.answer()
    await state.finish()


async def final_part_more(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(f'Great! Lets add more texts!')
    await callback.message.answer(f'Give me a new text please')
    await state.finish()
    await UploadText.Q1.set()




# what is the distance to the goal?



def register_handlers_text(dp:Dispatcher):
    dp.register_message_handler(start_uploading, commands='Upload_text', state="*")
    dp.register_message_handler(text_upload, state=UploadText.Q1)
    dp.register_callback_query_handler(text_understanding_yes, state=UploadText.Q2, text='yes')
    dp.register_callback_query_handler(text_understanding_no, state=UploadText.Q2, text='no')
    dp.register_callback_query_handler(give_me_translation, state=UploadText.Q3, text='give_me')
    dp.register_callback_query_handler(btn, state=UploadText.Q4, text='1')
    dp.register_callback_query_handler(btn, state=UploadText.Q4, text='2')
    dp.register_callback_query_handler(btn, state=UploadText.Q4, text='3')
    dp.register_callback_query_handler(btn, state=UploadText.Q4, text='4')
    dp.register_callback_query_handler(btn, state=UploadText.Q4, text='5')
    dp.register_callback_query_handler(btn, state=UploadText.Q4, text='6')
    dp.register_callback_query_handler(btn, state=UploadText.Q4, text='7')
    dp.register_callback_query_handler(btn, state=UploadText.Q4, text='8')
    dp.register_callback_query_handler(btn, state=UploadText.Q4, text='9')
    dp.register_callback_query_handler(display_more_words, state=UploadText.Q4, text='i_know')
    dp.register_callback_query_handler(finishing, state=UploadText.Q4, text='finish')
    dp.register_callback_query_handler(finishing, state=UploadText.Q4, text='just_finish')
    dp.register_callback_query_handler(final_part_out, state=UploadText.Q6, text='finish_here')
    dp.register_callback_query_handler(final_part_more, state=UploadText.Q6, text='more_text')

    # dp.register_message_handler(text_upload, state=UploadText.Q2)


