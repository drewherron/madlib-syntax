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
            # Adjust the table creation query to include sentence and tree_image_path
            cursor.execute("create table syntax_trees (id INTEGER PRIMARY KEY, sentence TEXT, tree_image_path TEXT, gif_image_path TEXT)")
        cursor.close()

    def select(self):
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM syntax_trees")
        return cursor.fetchall()

    def insert(self, sentence, tree_image_path, gif_image_path):
        """
        Inserts a new sentence and its corresponding tree image path into the database.
        """
        params = {'sentence': sentence, 'tree_image_path': tree_image_path, 'gif_image_path': gif_image_path}
        connection = sqlite3.connect(DB_FILE)
        cursor = connection.cursor()
        cursor.execute("insert into syntax_trees (sentence, tree_image_path, gif_image_path) VALUES (:sentence, :tree_image_path, :gif_image_path)", params)

        connection.commit()
        cursor.close()
        return True
