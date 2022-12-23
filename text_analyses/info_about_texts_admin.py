from dispatcher import BotDB
from text_analyses.countings import counting_words_main

all_texts = BotDB.get_all_admin_text()

all_texts_list = []

for i in all_texts:
    for n in i:
      all_texts_list.append(n)

connected = ' '.join(all_texts_list).split(',')

a, b, c = counting_words_main(connected[0])

print(len(all_texts))
print(len(a))
print(len(b))