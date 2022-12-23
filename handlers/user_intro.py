from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.dispatcher.storage import FSMContext
from aiogram import types
from dispatcher import BotDB
from extra.texts import bot_description, start_intro
from keyboards.usual import mainMenu
from states.intro_states import UploadText, IntroQuestions


#NOTES
# All long texts are in the separate file, so it is more convenient to edit them




#####################################################################################################
# BOT START WORKING

async def user_start(message: types.Message):
    User_id_info = message.from_user.id

    #####################################################################################################
    # New User INTO. Get the Info about the user to add to the DataBase

    if (not BotDB.user_exists(message.from_user.id)):

        await message.reply(start_intro.new_user)
        await message.answer(start_intro.new_user_1)
        await message.answer('How can I call you?')

        #####################################################################################################
        # HERE we initialize the FSM, to gather info for the database. The FSM functions are below

        await IntroQuestions.Q1.set()


    else:
        #####################################################################################################
        # That what old users will see
        text = message.text
        # BotDB.logging_session(user_id=User_id_info, action='user_start', text_id=0, text=text)


        await message.reply(start_intro.old_user, reply_markup=mainMenu)


#####################################################################################################
        # FSM to get the initial info from user


async def intro_name(message: types.Message, state: FSMContext):
    """
    The function ask user name to add for the first time to the database
    """
    name = message.text

    await message.reply(f'Nice to meet you {name}!')

    await message.answer('Do you have any goal on how many words do you want to learn? '
                         'So we can track your progress over time 👍')

    await state.update_data(Name=name)
    await state.update_data(User_id_info=message.from_user.id)
    await IntroQuestions.Q2.set()

async def set_goal(message: types.Message, state: FSMContext):
    """
      The function ask user Goal to add for the first time to the database
      """
    data = await state.get_data()
    Name = data.get('Name')
    User_id_info = data.get('User_id_info')


    if (message.text).isdigit():
        number = int(message.text)
        await message.answer(f'Great! So it is {number}. '
                             f'I wrote it down.\nWhen you know your goal, '
                             f'it is always easier to achieve it!')
        await message.answer(f'\nYour full answer is:'
                             f'\nName = {Name}'
                             f'\nGoal = {number}')
        await message.answer('Is it correct? Or you want to review? (y/n)')
        await state.update_data(goal = number)
        await IntroQuestions.Q3.set()
    else:
        number = 'Null'
        await state.update_data(goal=number)
        message.answer('I see, you can always add your goal into menu!')
        await message.answer(f'\nYour fool answer is:'
                         f'\nName = {Name}')
        await message.answer('Is it correct? Or you want to review? (y/n)')
        await IntroQuestions.Q3.set()

async def uploading_data(message: types.Message, state: FSMContext):
        """
          The function checks if everything is correct before adding to DB the first time
          """
        data = await state.get_data()
        Name = data.get('Name')
        User_id_info = data.get('User_id_info')
        Goal = data.get('goal')

        if (message.text).lower() in ['yes','y']:
            await message.answer('Great! I added you into my book of great friends!')
            await message.answer('If you ever decide to change your name or other info'
                                 ', you can do it in the settings.')
            await message.answer(f"Do you want me to introduce to this bot? (y/n)\n\n"
                                 f"Or you want to start using it right away?\nYou can always read about my functions in the info")
            await IntroQuestions.Q4.set()

            BotDB.add_user(User_id_info, Name, Goal)
            BotDB.logging_session(user_id=User_id_info, action='user_registered', text_id=0)
            list_of_texts = BotDB.get_all_texts()

            for i in list_of_texts:
                print(i[1])
                BotDB.user_texts_db(User_id_info, int(i[1]), 'not_read')


        else:
            await message.answer('I see, lets get start over again!')
            await  state.reset_state()
            await message.answer('How can I call you?')
            await IntroQuestions.Q1.set()

            #await intro_name(message="",state=IntroQuestions.Q1)

async def intro_bot(message: types.Message, state: FSMContext):
    text = message.text

    if text == 'y':
        await message.answer(bot_description.intro)
        await message.answer(bot_description.dictionary)
        await state.finish()
    else:
        await message.answer("Great! Let's practice then!", reply_markup=mainMenu)
        await state.finish()







def register_handlers_intro(dp:Dispatcher):
    dp.register_message_handler(user_start, commands=["start"], state="*")
    dp.register_message_handler(intro_name, state=IntroQuestions.Q1)
    dp.register_message_handler(set_goal, state=IntroQuestions.Q2)
    dp.register_message_handler(uploading_data, state=IntroQuestions.Q3)
    dp.register_message_handler(intro_bot, state=IntroQuestions.Q4)