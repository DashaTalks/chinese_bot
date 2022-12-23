from dispatcher import BotDB
from aiogram import types
from text_analyses.cleaning import ch_check

class PrintWord():
#this class take a translated word into the lang you need and send the message needed to the chat

    def __init__(self,status, message, word_id):
        self.status = status
        self.word_id = word_id

        if self.status == 'usual':
            self.message = message
        else:
            self.message = message.message

    async def give_meaning(self):
        if len(self.word_id) > 1:
            for i in self.word_id:
                # to improve efficiency u need to create two functions here. that will first check the lang, then translate
                if ch_check(i):
                    #text_pin = pinyin_jyutping_sentence.pinyin(i[0])
                    #await self.message.answer(str(i[0])+' '+str(text_pin))
                    await self.message.answer(str(i[0]))
                else:
                    await self.message.answer(i[0])

        else:
            try:
                word = self.word_id[0][0]
                await self.message.answer(word)
                #if ch_check(word):
                    #text_pin = pinyin_jyutping_sentence.pinyin(word)
                    #await self.message.answer(text_pin)
                #else:
                    #await self.message.answer(word)

            except Exception as e:
                print(e)
                print(self.word_id)
                await self.message.answer('Sorry, there is no such word in the library')


