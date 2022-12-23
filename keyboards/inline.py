from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

yes_no = InlineKeyboardMarkup(one_time_keyboard=True)
yes_btn = InlineKeyboardButton(text='Yes', callback_data='yes')
no_btn = InlineKeyboardButton(text="No, let's mark words I don't know", callback_data='no')

yes_no.add(yes_btn).add(no_btn)

yes_no_translation = InlineKeyboardMarkup()
give_me = InlineKeyboardButton(text='Give me the translation please', callback_data='give_me')
i_will_type = InlineKeyboardButton(text="I will type myself", callback_data='i_will_type')

yes_no_translation.add(give_me).add(i_will_type)


words_understanding = InlineKeyboardMarkup()
more = InlineKeyboardButton(text='I\'ve finished here, show me more words', callback_data='i_know')
one = InlineKeyboardButton(text="1", callback_data='1')
two = InlineKeyboardButton(text="2", callback_data='2')
three = InlineKeyboardButton(text="3", callback_data='3')
four = InlineKeyboardButton(text="4", callback_data='4')
five = InlineKeyboardButton(text="5", callback_data='5')
six = InlineKeyboardButton(text="6", callback_data='6')
seven = InlineKeyboardButton(text="7", callback_data='7')
eight = InlineKeyboardButton(text="8", callback_data='8')
nine = InlineKeyboardButton(text="9", callback_data='9')
#type_ = InlineKeyboardButton(text="I will type", callback_data='type')
changed = InlineKeyboardButton(text="Finish the process", callback_data='just_finish')
marked = InlineKeyboardButton(text="I've marked everything. Finish the process", callback_data='finish')


words_understanding.add(one,two,three,four,five,six,seven,eight,nine).add(marked).add(more).add(changed)


yes_no_more = InlineKeyboardMarkup(one_time_keyboard=True)
yes_btn = InlineKeyboardButton(text='I want to upload my text', callback_data='more_text')
read_btn = InlineKeyboardButton(text='Give me a text to read', callback_data='read_text')
no_btn = InlineKeyboardButton(text="No, thanks", callback_data='finish_here')

yes_no_more.add(yes_btn).add(read_btn).add(no_btn)


hsk_level = InlineKeyboardMarkup()
hsk_one = InlineKeyboardButton(text="HSK1", callback_data='HSK1')
hsk_two = InlineKeyboardButton(text="HSK2", callback_data='HSK2')
hsk_three = InlineKeyboardButton(text="HSK3", callback_data='HSK3')
hsk_four = InlineKeyboardButton(text="HSK4", callback_data='HSK4')
hsk_five = InlineKeyboardButton(text="HSK5", callback_data='HSK5')
hsk_six = InlineKeyboardButton(text="HSK6", callback_data='HSK6')

hsk_level.add(hsk_one, hsk_two, hsk_three, hsk_four, hsk_five, hsk_six)

