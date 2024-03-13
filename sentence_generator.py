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
        self.sentence_tree_pairs_arrows = load_sentence_tree_pairs("sentence_tree_pairs_arrows.json")

    def generate_filled_sentence_and_tree(self, arrow_flag):

        if arrow_flag:
            if random.random() > 0.0:
                selected_list = self.sentence_tree_pairs_arrows
            else:
                selected_list = self.sentence_tree_pairs
        else:
            selected_list = self.sentence_tree_pairs

        # Select a random sentence from the chosen list
        selected_pair = random.choice(selected_list)
        print(selected_pair)
        selected_theme = random.choice(self.themes)
        print(selected_theme)
        # Send skeleton to GPT, get JSON back
        custom_prompt = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Given the sentence structure: '{selected_pair['skeleton']}', generate a single word for each placeholder in angle brackets, to form a grammatically correct (natural-sounding) English sentence with a general theme: {selected_theme}. Return the answer in JSON format, with the original placeholders as keys and your new words as values. Provide no additional information or explanation."}
            ]
        print(custom_prompt)
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=custom_prompt
        )

        # The response from OpenAI is an object with a 'choices' list,
        # each choice has a 'message' object with 'content' attribute
        try:
            # Assuming the API correctly formats the response as expected
            words = json.loads(response.choices[0].message.content.strip())
            # In case ChatGPT keeps the bracket format
            normalized_words = {key.strip("<>"): value for key, value in words.items()}

        except json.JSONDecodeError:
            print("Failed to parse response as JSON.")
            return None, None, None

        # Use JSON to replace tags in sentence and tree
        filled_sentence = selected_pair["skeleton"]
        filled_tree = selected_pair["tree"]
        tree_movement = selected_pair["arrow"] if "arrow" in selected_pair else None

        for key, value in normalized_words.items():
            filled_sentence = filled_sentence.replace(f"<{key}>", value)
            filled_tree = filled_tree.replace(f"<{key}>", value)

        # Testing response
        print(response)

        return filled_sentence, filled_tree, tree_movement

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
    sentence, tree, movement = generator.generate_filled_sentence_and_tree()
    print("Generated Sentence:", sentence)
    print("Syntax Tree:", tree)
    print("Movement:", movement)
