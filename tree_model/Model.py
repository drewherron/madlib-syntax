class Model():
    def select(self):
        """
        Gets all entries from the database
        :return: List of dictionaries containing all rows of database
        """
        pass

    def insert(self, sentence, tree_image_path, gif_image_path):
        """
        Inserts entry into database
        :param sentence: String
        :param tree_image_path: String
        :param gif_image_path: String
        :return: True
        :raises: Database errors on connection and insertion
        """
        pass
