from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


btnMain = KeyboardButton('Main Menu')

# ---- MAIN MENU ----

btnStart = KeyboardButton('/Help') #Start working - intro + registration
btnUpload = KeyboardButton("/Upload_text") #upload new texts
btnReadText = KeyboardButton("/Read_a_text") #read text from the lib -> choose the text by the difficulty
btnReadTweets = KeyboardButton('Tweets 🐣')  #read tweets -> choose the text by the difficulty
btnStats = KeyboardButton('/My_stats') #show u your stats and insights
btnAbout = KeyboardButton('/About')  #about me
btnSettings = KeyboardButton('Settings') #-> change your name, goals, prefered difficulty
#btnDictionary = KeyboardButton('Learn Words') #-> change your name, goals, prefered difficulty

mainMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add( btnUpload, btnReadText,
                                     btnReadTweets, btnStats, btnAbout, btnSettings, btnStart,)

# ---- Settings ----

btnSettingsName = KeyboardButton('Change my name')
btnSettingsGoal = KeyboardButton('Change my language goal')

SettingsMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnSettingsName,btnSettingsGoal,btnMain)


# ---- ADMIN ----

btnUploadAdminText = KeyboardButton('/Upload_text_admin')

MenuAdminText = ReplyKeyboardMarkup(resize_keyboard=True).add(btnUploadAdminText)

# ---- HELP ----

about_help = KeyboardButton('Tell me, how to use the app?')
FAQ_help = KeyboardButton('Popular questions')
bug_help = KeyboardButton('How can I report the bug?')
back_help = KeyboardButton('Get back to main menu')

helpMarkup = ReplyKeyboardMarkup(resize_keyboard=True).add(about_help).add(FAQ_help).add(bug_help).add(back_help)



