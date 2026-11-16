# madlib-syntax

A small Flask web app for practicing X-bar syntax trees. It shows you a sentence, you draw its tree on paper, then click the GIF to reveal the correct tree and check your work.

## How it works

1. **Random template selection.** The app randomly picks a template from one of two sets. Each template is a sentence skeleton with part-of-speech placeholders (e.g. `The <noun1> <simple_past_verb> the <adjective> <noun2>.`), paired with a bracketed X-bar tree that uses the same placeholders.
   - `sentence_tree_pairs.json`: basic sentences with no movement. This set is always used when the "Allow movement" switch is off.
   - `sentence_tree_pairs_arrows.json`: questions with movement (e.g. T-to-C), including arrow coordinates. When the switch is on, roughly a third of sentences come from this set.
2. **Fill in the blanks.** `sentence_generator.py` sends the skeleton and a random theme from `themes.json` to the OpenAI API (GPT-4). The model returns a word for each placeholder as JSON, and those words go into both the sentence and the tree.
3. **Draw the tree.** `tree_image.py` parses the filled-in tree with NLTK and renders it to SVG with a [fork of svgling](https://github.com/drewherron/svgling/tree/leaf_edges) (`leaf_edges` branch), adding movement arrows when the template has them.
4. **Find a GIF.** `related_gif.py` searches Giphy for the sentence and falls back to `static/images/default.gif`.
5. **Show the page.** The sentence and GIF are displayed, and clicking the GIF reveals the tree. The "Allow movement" switch sets `?arrow_flag=true` in the URL.

Each result is also saved through `tree_model/` (Google Cloud Datastore, with a SQLite backend available). The app can serve saved entries instead of calling the APIs, but that's currently turned off (`database_chance = 0` in `app.py`).

## Running it

Requires `OPENAI_API_KEY` and `GIPHY_API_KEY`, plus the svgling fork cloned into `./svgling`. The Dockerfile handles the clone and runs the app with gunicorn. `cloudbuild.yaml` builds the image for Google Cloud Run.

```sh
pip install -r requirements.txt
git clone -b leaf_edges https://github.com/drewherron/svgling.git
python app.py   # http://localhost:5000
```

## Planned: madlib mode

Next, the plan is to remove both APIs. Instead of asking an LLM to fill in placeholders, the app will choose words at random from lists organized by part of speech (madlib-style). That means no API keys or per-request costs, and the trees can't be thrown off by a bad LLM response. The template/tree system stays the same.
