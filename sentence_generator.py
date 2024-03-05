from openai import OpenAI
import os
import json
import random

# This will be a class that sends a "skeleton" sentence to ChatGPT
# and returns a complete sentence AND tree
class SentenceGenerator:
    def __init__(self, openai_api_key):
        self.client = OpenAI(api_key=openai_api_key)
        #self.sentence_tree_pairs = load_sentence_tree_pairs()


    def generate_filled_sentence_and_tree(self):
        # Select a pair randomly from the file
#        selected_pair = random.choice(self.sentence_tree_pairs)
        # Send skeleton to GPT, get JSON back
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Given the sentence structure: The <adjective> <noun> <past_verb> <adverb>, please generate a grammatically correct word for each placeholder. Return the answer in JSON format, with the original placeholders as keys and your new words as values. Provide no additional information or explanation."}
            ]
        )

        # Testing response
        print(response)

        # Use JSON to replace tags in sentence and tree
        # TODO

        #return filled_sentence, filled_tree

def load_sentence_tree_pairs(filepath='sentence_tree_pairs.json'):
    with open(filepath, 'r') as file:
        pairs = json.load(file)
    return pairs

# For testing
if __name__ == '__main__':
    generator = SentenceGenerator(openai_api_key=os.getenv('OPENAI_API_KEY'))
#    sentence, tree = generator.generate_filled_sentence_and_tree()
    generator.generate_filled_sentence_and_tree()    
#    print("Generated Sentence:", sentence)
#    print("Syntax Tree:", tree)
