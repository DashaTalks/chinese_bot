from text_analyses.cleaning import no_eng, cleaning, unique_my_words, dict_creation, sorting_dict, eng_check


def goal(words_you_know):
    user_goal = 3000
    left = user_goal - words_you_know
    percent_you_did = str(round((words_you_know/user_goal)*100))+'%'
    percent_left = str(round((left/user_goal)*100))+'%'
    return percent_you_did, percent_left, left


def counting_words_main(text):
    unique_words = []
    full_dict = []

    no_eng_words = no_eng(text)
    united_text = []

    for res in text:
        res = str(res)
        if eng_check(res) == False:
            if res not in ['ǒ', 'í','ò','ǎ','ǐ', 'à', 'ǔ','é','ā',
                           'ō','ì','è','ó','á','ú','ù','ī','ě','ē','ū','ǚ']:
                united_text.append(res)

    united_text = (''.join(united_text).split(','))[0]

    clean_text = cleaning(no_eng_words)
    unique_my_words(clean_text, unique_words, full_dict)

    how_many_unique = len(unique_words)
    if goal:
        percent_you_did, percent_left, left = goal(how_many_unique)

    dictOfWords = dict_creation(unique_words, full_dict)
    sorted_dict = sorting_dict(dictOfWords)

    return full_dict, unique_words, united_text
