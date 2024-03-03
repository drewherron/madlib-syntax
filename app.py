"""
A simple guestbook flask app.
"""
import flask, os
from sentence_generator import SentenceGenerator
from flask.views import MethodView
from index import Index
from sign import Sign

app = flask.Flask(__name__)
generator = SentenceGenerator(openai_api_key=os.getenv('OPENAI_API_KEY'))
model = get_model()


app.add_url_rule('/',
                 view_func=Index.as_view('index'),
                 methods=["GET"])

app.add_url_rule('/sign/',
                 view_func=Sign.as_view('sign'),
                 methods=['GET', 'POST'])

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT',5000)))
