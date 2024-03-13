import sqlite3
from .Model import Model

DB_FILE = 'entries.db'    # file for our Database

class model(Model):
    def __init__(self):
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        try:
            cursor.execute("select count(rowid) from syntax_trees")
        except sqlite3.OperationalError:
            cursor.execute("create table syntax_trees (id INTEGER PRIMARY KEY, sentence TEXT, tree_image_path TEXT, gif_image_path TEXT, arrow_flag INTEGER)")
        cursor.close()

    def select(self):
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM syntax_trees")
        return cursor.fetchall()

    def insert(self, sentence, tree_image_path, gif_image_path, arrow_flag):
        """
        Inserts a new sentence with image and arrow data into database.
        """
        params = {'sentence': sentence, 'tree_image_path': tree_image_path, 'gif_image_path': gif_image_path, 'arrow_flag': arrow_flag}
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("insert into syntax_trees (sentence, tree_image_path, gif_image_path, arrow_flag) VALUES (:sentence, :tree_image_path, :gif_image_path, :arrow_flag)", params)

        connection.commit()
        cursor.close()
        return True

    def select_random(self, arrow_flag=None):
        """
        Selects a random entry from the database.
        """
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        query = "SELECT sentence, tree_image_path, gif_image_path FROM syntax_trees"

        # If arrow_flag is False, only select entries where arrow_flag is also False
        if arrow_flag == False:
            query += " WHERE arrow_flag = 0"

        query += " ORDER BY RANDOM() LIMIT 1"

        cursor.execute(query)
        result = cursor.fetchone()
        connection.close()
        return result
