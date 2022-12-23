--
-- File generated with SQLiteStudio v3.3.3 on Чт май 5 15:36:01 2022
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: texts
CREATE TABLE texts (id INTEGER PRIMARY KEY, user_id INTEGER REFERENCES users (id) ON DELETE CASCADE NOT NULL, text_full TEXT NOT NULL, date_added DATETIME DEFAULT ((DATETIME('now'))) NOT NULL);
INSERT INTO texts (id, user_id, text_full, date_added) VALUES (1, 2, 'text', '2022-05-04 17:55:23');
INSERT INTO texts (id, user_id, text_full, date_added) VALUES (2, 2, 'hey there!', '2022-05-04 18:00:46');

-- Table: user_words
CREATE TABLE user_words (user_id INTEGER REFERENCES users (id) NOT NULL, word_id INTEGER REFERENCES words (word_id) NOT NULL, status VARCHAR, word_user_pair_id INTEGER PRIMARY KEY);

-- Table: users
CREATE TABLE users (id INTEGER PRIMARY KEY NOT NULL, user_id INTEGER NOT NULL UNIQUE, name VARCHAR, lang_goal INTEGER, join_date DATETIME NOT NULL DEFAULT ((DATETIME('now'))));
INSERT INTO users (id, user_id, name, lang_goal, join_date) VALUES (1, 1000, NULL, NULL, '2022-05-04 12:23:34');
INSERT INTO users (id, user_id, name, lang_goal, join_date) VALUES (2, 266287743, NULL, NULL, '2022-05-04 12:40:17');

-- Table: words
CREATE TABLE words (word_id INTEGER PRIMARY KEY NOT NULL, word_ch VARCHAR NOT NULL, word_trad VARCHAR NOT NULL, freq NUMERIC, transl_ru VARCHAR NOT NULL);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
