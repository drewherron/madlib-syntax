import flask
from flask.views import MethodView
from sentence_generator import SentenceGenerator
from tree_image import generate_syntax_tree_image
from related_gif import fetch_gif_url
from tree_model import get_model
import requests
import random
import time
import uuid
import os

app = flask.Flask(__name__)
generator = SentenceGenerator(openai_api_key=os.getenv('OPENAI_API_KEY'))
model = get_model()

@app.route('/')
def index():
    arrow_flag = flask.request.args.get('arrow_flag', 'false').lower() in ['true', '1', 'yes']
    database_chance = 0

    # Chance to use database instead of APIs
    if random.random() < database_chance:
        print("Selecting random entry from database")
        sentence, tree_image_path, related_gif_url = model.select_random(arrow_flag=arrow_flag if arrow_flag else None)
        # TODO catch retrieval error here?

    # Use the APIs
    else:
        sentence, tree_structure, tree_movement = None, None, None
        retry_delay = 2
        max_retries = 5
        attempts = 0

        while sentence is None and attempts < max_retries:
            sentence, tree_structure, tree_movement = generator.generate_filled_sentence_and_tree(arrow_flag)
            if sentence is None:
                print("Failed fetching sentence, retrying...")
                time.sleep(retry_delay)
                attempts += 1

        tree_image_path = f"static/images/syntax_tree_{uuid.uuid4()}.svg"
        generate_syntax_tree_image(tree_structure, tree_movement, tree_image_path)

        #related_gif_url = fetch_gif_url(sentence)
        related_gif_url = "https://media.giphy.com/media/tU2mV8ALzJEdXAAwRo/giphy.gif"

        # Send data to the model
        model.insert(sentence, tree_image_path, related_gif_url, arrow_flag)

    # Render the index page
    return flask.render_template('index.html', sentence=sentence, tree_image_path=tree_image_path, related_gif_url=related_gif_url, arrow_flag=arrow_flag)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT',5000)))
