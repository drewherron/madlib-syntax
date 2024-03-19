from datetime import datetime
from google.cloud import datastore

def from_datastore(entity):
    """
    Translates Datastore results into the format expected by the
    application.

    Datastore typically returns:
        [Entity{key: (kind, id), prop: val, ...}]

    This returns:
        [sentence, tree_image_path, gif_image_path, arrow_flag]
    """
    if not entity:
        return None
    if isinstance(entity, list):
        entity = entity.pop()

    return [
        entity.get('sentence'),
        entity.get('tree_image_path'),
        entity.get('gif_image_path'),
        entity.get('arrow_flag')
    ]

class model:
    def __init__(self):
        self.client = datastore.Client('your_project_id_here')
        self.kind = 'SyntaxTree'

    def select(self):
        query = self.client.query(kind=self.kind)
        entities = list(map(from_datastore, query.fetch()))
        return entities

    def insert(self, sentence, tree_image_path, gif_image_path, arrow_flag):
        key = self.client.key(self.kind)
        entity = datastore.Entity(key=key)
        entity.update({
            'sentence': sentence,
            'tree_image_path': tree_image_path,
            'gif_image_path': gif_image_path,
            'arrow_flag': arrow_flag,
        })
        self.client.put(entity)
        return True

    def select_random(self, arrow_flag=None):
        """
        Selects a random entry from Datastore. Note: Datastore does not support
        ORDER BY RANDOM(), so this fetches all relevant entities and selects one at random
        in application code. For large datasets, consider an alternative approach.
        """
        query = self.client.query(kind=self.kind)
        if arrow_flag is not None:
            query.add_filter('arrow_flag', '=', arrow_flag)
        entities = list(query.fetch())

        if entities:
            from random import choice
            selected = choice(entities)  # Randomly select one entity
            return from_datastore(selected)
        return None
