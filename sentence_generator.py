from openai import OpenAI
import json
import random

# This will be a class that sends a "skeleton" sentence to ChatGPT
# and returns a complete sentence AND tree
class SentenceGenerator:
    def __init__(self, openai_api_key):
        self.client = OpenAI(api_key=openai_api_key)

    def generate_filled_sentence_and_tree(self):
        # Select a pair randomly from the file
        # Send skeleton to GPT, get JSON back
        # Use JSON to replace tags in sentence and tree
        return filled_sentence, filled_tree

def load_sentence_tree_pairs(filepath='sentence_tree_pairs.json'):
        with open(filepath, 'r') as file:
        pairs = json.load(file)
    return pairs
