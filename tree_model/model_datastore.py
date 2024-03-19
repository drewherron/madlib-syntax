from google.cloud import datastore
from datetime import datetime


def from_datastore(entity):
    return {
        'sentence': entity.get('sentence'),
        'tree_image_path': entity.get('tree_image_path'),
        'gif_image_path': entity.get('gif_image_path'),
        'arrow_flag': entity.get('arrow_flag')
    }

class model(Model):
    def __init__(self):
        self.client = datastore.Client('syntax-trees')
        self.kind = 'SyntaxTree'

    def select(self):
        query = self.client.query(kind=self.kind)
        entities = list(map(from_datastore, query.fetch()))
        return entities

    def insert(self, sentence, tree_image_path, gif_image_path, arrow_flag):
        """
        Inserts a new sentence with image and arrow data into database.
        """
        key = self.client.key(self.kind)
        entity = datastore.Entity(key=key)
        entity.update({
            'sentence': sentence,
            'tree_image_path': tree_image_path,
            'gif_image_path': gif_image_path,
            'arrow_flag': arrow_flag,
            'created_at': datetime.utcnow() 
        })
        self.client.put(entity)
        return True

    def select_random(self, arrow_flag=None):
        """
        Selects a random entry from the database.
        """
        query = self.client.query(kind=self.kind)
        if arrow_flag is not None:
            query.add_filter('arrow_flag', '=', arrow_flag)
        entities = list(query.fetch())
        if entities:
            from random import choice
            selected_entity = choice(entities)
            return from_datastore(selected_entity)
        return None, None, None
