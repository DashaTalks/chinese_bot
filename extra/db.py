import sqlite3
import mysql.connector
from mysql.connector import Error



class BotDB:



    def __init__(self):

        try:
            self.connection = mysql.connector.connect(host='localhost',
                                                      database='words',
                                                      user='root',
                                                      password='admin')
            if self.connection.is_connected():
                self.db_Info = self.connection.get_server_info()
                print("Connected to MySQL Server version ", self.db_Info)
                self.cursor = self.connection.cursor(buffered=True)
                self.cursor.execute("select database();")
                self.record = self.cursor.fetchone()
                print("You're connected to database: ", self.record)
        except Error as e:
            print("Error while connecting to MySQL", e)

    ################################################################
    # USER

    def user_exists(self, user_id):
        """Проверяем, есть ли юзер в базе"""
        self.cursor.execute(f"SELECT `tg_user_id` FROM user WHERE `tg_user_id` = {user_id}")
        result = self.cursor.fetchall()

        return bool(len(result))

    def add_user(self, user_id, name, goal):
        """Добавляем юзера в базу"""
        self.cursor.execute("INSERT INTO user (tg_user_id, user_name, lang_goal) VALUES (%s,%s,%s)", (user_id, name, goal))
        return self.connection.commit()

    def get_log_id(self, user_id):
        """Достаем id юзера в базе по его user_id"""
        result = self.cursor.execute("SELECT `` FROM `user` WHERE `user_id` = %s", (user_id,))
        return result.fetchone()[0]

    def user_texts_db(self, user_id, text_id,status):
        """Добавляем юзера в базу"""
        self.cursor.execute("INSERT INTO user_has_admin_texts (user_tg_user_id, admin_texts_admin_text_id, status) VALUES"
                            " (%s,%s,%s)", (user_id, text_id,status))
        return self.connection.commit()

    ################################################################
    # Logging

    def logging_session(self, user_id, action, text_id=0, text=''):
        if text_id != 0:
            text_to_add = ''
        else:
            text_to_add = text
        self.cursor.execute("INSERT INTO `logging` (user_tg_user_id, action, text_id, text) VALUES (%s,%s, %s, %s)", (user_id, action, text_id, text_to_add))
        id = self.cursor.lastrowid

        # print("#"*60)
        # #self.connection.commit()
        return self.connection.commit(), id

    def get_goal(self, user_id):
        """Достаем id юзера в базе по его user_id"""
        result = self.cursor.execute("SELECT `id` FROM `user` WHERE `user_id` = %s", (user_id,))
        return result.fetchone()[0]

    ################################################################
    # WORDS

    def get_word_id(self, word):
        '''get the id of the chinese word'''
        self.cursor.execute("SELECT ch_w_id FROM ch_words where "
                            "word_ch = %s ", (word,))
        word_id = self.cursor.fetchall()
        return word_id


    def get_all_texts(self):
        self.cursor.execute('SELECT list_of_words, admin_text_id, text_full, hsk,title, title_eng FROM words.admin_texts_full'
                            ' left join user_has_admin_texts on admin_text_id = admin_texts_admin_text_id ' )
        list_of_texts = self.cursor.fetchall()
        return list_of_texts

    def get_all_texts_for_a_user(self, user):
        self.cursor.execute(
            'SELECT list_of_words, admin_text_id, text_full, hsk,title, title_eng FROM words.admin_texts_full'
            ' left join user_has_admin_texts on admin_text_id = admin_texts_admin_text_id '
            'where status = "not_read" and user_tg_user_id = (%s)', (user,))
        list_of_texts = self.cursor.fetchall()
        return list_of_texts


    def text_update(self, admin_text_id, text_full, hsk, title, url, title_eng, list_of_words):
        self.cursor.execute('INSERT INTO `admin_texts_full`'
                            '(admin_text_id, text_full, hsk, title, url, title_eng, list_of_words)'
                            ' VALUES (%s,%s,%s,%s,%s,%s,%s)', (admin_text_id, text_full, hsk, title, url,
                                                                   title_eng, list_of_words))
        return self.connection.commit()

    def get_text_info(self):
        self.cursor.execute('SELECT admin_text_id, text_full, hsk, title, url,'
                            'title_eng, dateAdded FROM `admin_texts`')
        texts = self.cursor.fetchall()
        return texts

    def check_if_in_unique(self, word):
        self.cursor.execute("SELECT ch_w_id FROM ch_words where word_ch = %s ", (word,))
        word_id = self.cursor.fetchall()
        return bool(len(word_id))

    def check_status_learning(self, word_id):
        self.cursor.execute("SELECT status FROM unique_words where ch_words_ch_w_id = %s ", (word_id,))
        status = self.cursor.fetchall()
        return status

    def word_text_pair(self, word_id, text_id):
        self.cursor.execute("INSERT INTO ch_words_has_texts_from_users "
                            "(ch_words_ch_w_id, texts_from_users_tx_from_u) VALUES (%s,%s)", (word_id, text_id))
        # id = self.cursor.lastrowid

        return self.connection.commit()

    def unique_word_text_pair(self, word_id, user_id, status):
        self.cursor.execute("INSERT INTO unique_words "
                            "(ch_words_ch_w_id, status, user_id) VALUES (%s,%s,%s)", (word_id, status, user_id))
        # id = self.cursor.lastrowid

        return self.connection.commit()

    def update_learning_status_part_one(self, word_id):
        self.cursor.execute('DELETE FROM unique_words WHERE ch_words_ch_w_id = %s'
                            , (word_id,))

        return self.connection.commit()
    def update_learning_status_part_two(self, word_id):
        self.cursor.execute('insert into unique_words  (ch_words_ch_w_id,`status`) '
                            'VALUES (%s, "Know")', (word_id,))

        return self.connection.commit()


    def word_is_known_by_user(self, word, user):
        """
        it checks the words that user knows and return frequencies in the user dict
        """
        self.cursor.execute('SELECT DISTINCT ch_w_id, freq, count(ch_w_id), pinyin as frequency_in_dict FROM ch_words JOIN ch_words_has_texts_from_users chtxt ON ch_w_id = chtxt.ch_words_ch_w_id '
                            'JOIN texts_from_users ON chtxt.texts_from_users_tx_from_u = texts_from_users.tx_from_u '
                            'JOIN logging_has_texts_from_users logtxt ON texts_from_users.tx_from_u = logtxt.texts_from_users_tx_from_u '
                            'JOIN logging ON logging_log_id = log_id '
                            'where word_ch = %s and user_tg_user_id = %s', (word, user))
        word_id = self.cursor.fetchall()
        return word_id

    def get_unknown_freq(self, word):
        """
        check the frequencies in the library of the new user
        """
        self.cursor.execute("SELECT freq, pinyin FROM ch_words where word_ch = %s ", (word,))
        word_id = self.cursor.fetchall()
        return word_id

    def get_unique_words(self, user_id):
        """
        Give you all unique words
        """
        query = "SELECT word_ch, freq FROM `ch_words` " \
                "inner join `unique_words` on ch_w_id = ch_words_ch_w_id  " \
                 "where user_id = (%s) and status = 'Know'"
        value = user_id
        self.cursor.execute(query, (value,))
        list_of_words = self.cursor.fetchall()
        return list_of_words

    def get_unique_words_two(self,user):
        """
        it checks the words that user knows and return frequencies in the user dict
        """
        self.cursor.execute('SELECT ch_w_id, freq, count(ch_w_id), pinyin as frequency_in_dict FROM ch_words JOIN ch_words_has_texts_from_users chtxt ON ch_w_id = chtxt.ch_words_ch_w_id '
                            'JOIN texts_from_users ON chtxt.texts_from_users_tx_from_u = texts_from_users.tx_from_u '
                            'JOIN logging_has_texts_from_users logtxt ON texts_from_users.tx_from_u = logtxt.texts_from_users_tx_from_u '
                            'JOIN logging ON logging_log_id = log_id '
                            'where user_tg_user_id = %s '
                            'group by ch_w_id', (user,))
        word_id = self.cursor.fetchall()
        return word_id

    def check_if_word_in_unique(self, word_id, user):
        self.cursor.execute("SELECT ch_words_ch_w_id FROM unique_words where ch_words_ch_w_id = %s and user_id = %s", (word_id, user))
        answer = self.cursor.fetchall()
        return answer


    ################################################################
    # TRANSLATION

    def ch_to_eng(self, word:str) -> str:
        self.cursor.execute("SELECT translation FROM eng LEFT JOIN ch_eng ON eng.eng_id = ch_eng.eng_id"
                            " LEFT JOIN ch_words ON ch_eng.ch_id = ch_words.ch_w_id "
                            " where word_ch = %s ",(word,))
        word_id = self.cursor.fetchall()
        return word_id

    def eng_to_ch(self, word):
        self.cursor.execute("SELECT word_ch FROM ch_words LEFT JOIN ch_eng ON ch_words.ch_w_id = ch_eng.ch_id"
                            " LEFT JOIN eng ON eng.eng_id = ch_eng.eng_id "
                            " where translation LIKE %s ",(word,))
        word_id = self.cursor.fetchall()
        return word_id

    def text_status_update(self, text, user, status) :
        self.cursor.execute("INSERT INTO user_has_admin_texts (user_tg_user_id, admin_texts_admin_text_id, status)"
                            " VALUES (%s,%s,%s)", (text,user,status))

        return self.connection.commit()

    def text_status_update_two(self, user, text):
        self.cursor.execute("UPDATE user_has_admin_texts "
                            "SET status = 'read' "
                            "where admin_texts_admin_text_id = (%s) and user_tg_user_id = (%s);", (int(text), int(user)))

        return self.connection.commit()

    ################################################################
    # Work with texts

    def add_text(self, text):
        query = "INSERT INTO texts_from_users (text_full) VALUES (%s)"
        value = text
        self.cursor.execute(query, (value,))
        id = self.cursor.lastrowid
        return self.connection.commit(), id

    def user_text(self, log_id, text_id):
        self.cursor.execute("INSERT INTO logging_has_texts_from_users (logging_log_id, texts_from_users_tx_from_u) "
                            "VALUES (%s, %s)", (log_id, text_id))
        id = self.cursor.lastrowid

        return self.connection.commit(), id

    def text_by_admin(self, title, text, hsk, url, eng_title):
        self.cursor.execute("INSERT INTO admin_texts (text_full, hsk, title, url, title_eng) VALUES (%s, %s, %s, %s, %s)", (text, hsk, title,  url, eng_title))

        return self.connection.commit()

    def get_rand_text(self):
        sql_q = 'select * from admin_texts order by rand() limit 1;'
        self.cursor.execute(sql_q)
        txt = self.cursor.fetchall()
        return txt

    def get_all_admin_text(self):
        self.cursor.execute("SELECT text_full FROM admin_texts")
        texts = self.cursor.fetchall()
        return texts




    ################################################################
    # GET ANALYTICS

    # def get_word_id(self, word):
    #     self.cursor.execute("SELECT ch_w_id, word_ch FROM ch_words where word_ch = %s ",(word,))
    #     remaining_rows = self.cursor.fetchall()
    #     return remaining_rows

    def get_data_after_adding_text(self, user_id):
        """
        Give you the number of words a person know
        """
        query = "SELECT count(DISTINCT ch_words_ch_w_id) FROM ch_words_has_texts_from_users c " \
                "inner join texts_from_users on c.texts_from_users_tx_from_u = texts_from_users.tx_from_u  " \
                "inner join logging_has_texts_from_users l on l.texts_from_users_tx_from_u = texts_from_users.tx_from_u   " \
                "inner join logging on logging.log_id = logging.log_id    " \
                "inner join user on logging.user_tg_user_id = user.tg_user_id   " \
                "where tg_user_id = (%s)"
        value = user_id
        self.cursor.execute(query, (value,))
        number_of_words = self.cursor.fetchall()
        return number_of_words


    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()


