import spacy
import re

from dispatcher import BotDB

nlp = spacy.load('zh_core_web_md')

# nlp = spacy.load("zh_core_web_sm")

def no_eng(context):
    filtrate = re.compile(u'[^\u4E00-\u9FFF]')  # non-Chinese unicode range
    context = filtrate.sub(r'', context)  # remove all non-Chinese characters
    # context = context.encode("utf-8") # convert unicode back to str
    return context



def no_ch(context):
    filtrate = re.compile(u'[^\u0000-\u007F]')  # non-Chinese unicode range
    context = filtrate.sub(r'', context)  # remove all non-Chinese characters
    # context = context.encode("utf-8") # convert unicode back to str
    return context

def eng_check(context):
    counter = 0
    while counter < len(context):
        for i in context:
            if u'\u0000' <= i <= u'\u007F':
                answer = True
            else:
                answer = False

            if answer == False:
                return False

        counter += 1
    return True

def ch_check(context):
    counter = 0
    while counter < len(context):
        for i in context:
            if u'\u4E00' <= i <= u'\u9FFF':
                answer = True
            else:
                answer = False

            if answer == False:
                return False

        counter += 1
    return True





def cleaning(text):
    doc = nlp(text)
    clean_word = []
    for token in doc:
        clean_word.append(str(token))
    for word in clean_word:
        if word in ['，','。','']:
            clean_word.remove(word)

    for i in clean_word:
        result = BotDB.get_word_id(i)
        if len(result) < 1:
            if len(i) > 1:
                clean_word.remove(i)
                for let in i:
                    clean_word.append(let)



    return clean_word


def unique_my_words(lists, my_list_of_words, all_words):
    for word in lists:
        all_words.append(word)
        if word not in my_list_of_words:
            my_list_of_words.append(word)
    return my_list_of_words,all_words

def dict_creation(my_list_of_words: object, all_words: object) -> object:
    dictOfWords = {i: 0 for i in my_list_of_words}
    for word in all_words:
        dictOfWords[word] += 1

    return dictOfWords


def sorting_dict(dic):
    unsorted_list = [[k, v] for k, v in dic.items()]
    sorted_by_number = sorted(unsorted_list, key=lambda tup: tup[1], reverse=True)
    return sorted_by_number

def what_hsk(word_list,*hsk_list):
    for hsk_level in hsk_list:
        list_of_words = [el[0] for el in hsk_level]
        level_of_hsk = hsk_level[0][1]
        for word in word_list:
            if word[0] in list_of_words:
                word.append(level_of_hsk)
    return word_list