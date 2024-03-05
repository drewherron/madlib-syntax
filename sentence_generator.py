from openai import OpenAI
import os
import json
import random

# This will be a class that sends a "skeleton" sentence to ChatGPT
# and returns a complete sentence AND tree
class SentenceGenerator:
    def __init__(self, openai_api_key):
        self.client = OpenAI(api_key=openai_api_key)
        self.themes = load_themes()
        self.sentence_tree_pairs = load_sentence_tree_pairs()


    def generate_filled_sentence_and_tree(self):
        # Select a pair randomly from the file
        selected_pair = random.choice(self.sentence_tree_pairs)
        print(selected_pair)
        selected_theme = random.choice(self.themes)
        print(selected_theme)
        # Send skeleton to GPT, get JSON back
        my_prompt = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Given the sentence structure: '{selected_pair['skeleton']}', generate a word for each placeholder in angle brackets, to form a grammatically correct sentence with a general theme: {selected_theme}. Return the answer in JSON format, with the original placeholders as keys and your new words as values. Provide no additional information or explanation."}
            ]
        print(my_prompt)
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=my_prompt
        )

        # The response from OpenAI is an object with a 'choices' list,
        # each choice has a 'message' object with 'content' attribute
        try:
            # Assuming the API correctly formats the response as expected
            words = json.loads(response.choices[0].message.content.strip())
        except json.JSONDecodeError:
            print("Failed to parse response as JSON.")
            return None, None

        # Use JSON to replace tags in sentence and tree
        filled_sentence = selected_pair["skeleton"]
        filled_tree = selected_pair["tree"]

        for key, value in words.items():
            filled_sentence = filled_sentence.replace(f"<{key}>", value)
            filled_tree = filled_tree.replace(f"<{key}>", value)

        # Testing response
        print(response)

        return filled_sentence, filled_tree

def load_themes(filepath='themes.json'):
    with open(filepath, 'r') as file:
        themes = json.load(file)
    return themes

def load_sentence_tree_pairs(filepath='sentence_tree_pairs.json'):
    with open(filepath, 'r') as file:
        pairs = json.load(file)
    return pairs

# For testing
if __name__ == '__main__':
    generator = SentenceGenerator(openai_api_key=os.getenv('OPENAI_API_KEY'))
    sentence, tree = generator.generate_filled_sentence_and_tree()
    print("Generated Sentence:", sentence)
    print("Syntax Tree:", tree)
