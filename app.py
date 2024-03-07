import flask
from flask.views import MethodView
from sentence_generator import SentenceGenerator
from tree_image import generate_syntax_tree_image
#from tree_model import get_model
import uuid
import os

app = flask.Flask(__name__)
generator = SentenceGenerator(openai_api_key=os.getenv('OPENAI_API_KEY'))
#model = get_model()

@app.route('/')
def index():

    sentence, tree_structure, tree_movement = generator.generate_filled_sentence_and_tree()

    tree_image_path = f"static/images/syntax_tree_{uuid.uuid4()}.svg"
    generate_syntax_tree_image(tree_structure, tree_movement, tree_image_path)

    # ?
    #model.insert(sentence, tree_image_path) #gif_path?

    # Render the index page with the sentence and path to the syntax tree image
    return flask.render_template('index.html', sentence=sentence, tree_image_path=tree_image_path)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT',5000)))
