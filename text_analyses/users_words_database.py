from dispatcher import BotDB


def adding_all_words_to_db(words, text_id):
    counter = 1
    for i in words:
        counter = counter+1
        word_id = BotDB.get_word_id(i)
        try:
            word_id_new = word_id[0][0]
            BotDB.word_text_pair(word_id_new, text_id[1])
            status_check = BotDB.check_status_learning(word_id_new)
            if status_check[0][0] == 'learning':
                BotDB.update_learning_status_part_one(word_id_new)
                BotDB.update_learning_status_part_two(word_id_new)


        except Exception as e:
            if len(i) > 1:
                for char in i:
                    word_id = BotDB.get_word_id(char)
                    if len(word_id) > 0:
                        word_id_new = word_id[0][0]
                        BotDB.word_text_pair(word_id_new, text_id[1])
                        status_check = BotDB.check_status_learning(word_id_new)
                        if status_check == 'learning':
                            BotDB.update_learning_status(word_id_new)


#it should check if the word is already there
def adding_unique_words_to_db(unique, user_id, status):
        for unique_word in unique:
            word_id = BotDB.get_word_id(unique_word)
            try:
                word_id_new = word_id[0][0]
                if len(BotDB.check_if_word_in_unique(word_id_new,user_id)) < 1:
                    BotDB.unique_word_text_pair(word_id_new, user_id, status )

            except Exception as e:
                if len(unique_word) > 1:
                    for char in unique_word:
                         word_id = BotDB.get_word_id(char)
                         if len(word_id) > 0:
                                        try:
                                            word_id_new = word_id[0][0]
                                            if len(BotDB.check_if_word_in_unique(word_id_new, user_id))<1:
                                                BotDB.unique_word_text_pair(word_id_new, status, user_id)
                                        except:
                                                pass
