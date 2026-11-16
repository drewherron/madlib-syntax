"""Fill sentence/tree templates with random words from the lexicon.

Placeholder format, used identically in a template's skeleton and tree:

    <category.form#n>   e.g. <noun.sg#1>, <vt.past#1>
    <category#n>        for categories with no forms, e.g. <adj#2>, <modal#1>

The index n ties the skeleton slot to the matching tree leaf. Within one
template, different indices of the same category get different words, so
<noun.sg#1> and <noun.pl#2> are never the same noun.

Categories (see lexicon.json):
    noun     forms: sg, pl
    vt       transitive verb          forms: base, 3sg, past, prog
    vi       intransitive verb        (same forms)
    vc       verb taking a that-clause (think, say)
    vpsy     verb taking a clausal subject (annoy, surprise)
    adj, adv (manner), adv_deg (very, quite), name, pron, poss,
    modal, conj (subordinating), prep, det_sg, det_pl
    a        the article; becomes "a" or "an" depending on the next word

Verbs live in one "verb" list; each verb's "frames" say which of
vt/vi/vc/vpsy it can fill.

lexicon.json is generated: edit words.txt and run build_lexicon.py.
"""
import json
import random
import re

PLACEHOLDER = re.compile(r"<([a-z_]+)(?:\.([a-z0-9]+))?#(\d+)>")
NOUN_FORMS = ("sg", "pl")
VERB_FORMS = ("base", "3sg", "past", "prog")
VERB_FRAMES = ("vt", "vi", "vc", "vpsy")

# Words where spelling and the a/an sound disagree.
A_EXCEPTIONS = ("uni", "use", "usu", "uti", "eu", "one", "once")
AN_EXCEPTIONS = ("hour", "honest", "honor", "heir")


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_templates(path="templates.json"):
    return load_json(path)


def load_lexicon(path="lexicon.json"):
    return load_json(path)


def article_for(word):
    w = word.lower()
    if w.startswith(AN_EXCEPTIONS):
        return "an"
    if w.startswith(A_EXCEPTIONS):
        return "a"
    return "an" if w[:1] in "aeiou" else "a"


def candidates(lexicon, category):
    """Return the list of entries that can fill a category."""
    if category in VERB_FRAMES:
        return [v for v in lexicon["verb"] if category in v["frames"]]
    if category not in lexicon:
        raise KeyError(f"Unknown placeholder category: {category}")
    return lexicon[category]


def inflect(entry, category, form):
    if category == "noun":
        if form not in NOUN_FORMS:
            raise KeyError(f"Unknown noun form: {form}")
        return entry[NOUN_FORMS.index(form)]
    if category in VERB_FRAMES:
        if form not in VERB_FORMS:
            raise KeyError(f"Unknown verb form: {form}")
        return entry[form]
    if form is not None:
        raise KeyError(f"Category {category} has no forms (got .{form})")
    return entry


def fill_template(template, lexicon, rng=random):
    """Return (sentence, tree, arrows) with every placeholder filled."""
    skeleton, tree = template["skeleton"], template["tree"]
    tokens = list(dict.fromkeys(m.group(0) for m in PLACEHOLDER.finditer(skeleton)))

    # Pick one lexicon entry per (category, index), distinct within a category.
    chosen, used = {}, {}
    values = {}
    for tok in tokens:
        cat, form, idx = PLACEHOLDER.fullmatch(tok).groups()
        if cat == "a":
            continue
        key = (cat, idx)
        if key not in chosen:
            pool = [e for e in candidates(lexicon, cat) if e not in used.get(cat, [])]
            chosen[key] = rng.choice(pool)
            used.setdefault(cat, []).append(chosen[key])
        values[tok] = inflect(chosen[key], cat, form)

    # Articles depend on the word that follows them in the sentence.
    partial = skeleton
    for tok, word in values.items():
        partial = partial.replace(tok, word)
    for tok in tokens:
        if tok.startswith("<a#"):
            following = re.search(re.escape(tok) + r"\s+(\S+)", partial).group(1)
            values[tok] = article_for(following)

    # Capitalize the first word if it comes from a placeholder.
    first = PLACEHOLDER.match(skeleton)
    if first:
        tok = first.group(0)
        values[tok] = values[tok][:1].upper() + values[tok][1:]

    sentence, filled_tree = skeleton, tree
    for tok, word in values.items():
        sentence = sentence.replace(tok, word)
        filled_tree = filled_tree.replace(tok, word)

    return sentence, filled_tree, template.get("arrow")


def random_sentence(templates, lexicon, allow_movement=False, movement_chance=1/3, rng=random):
    """Pick a template and fill it. With movement allowed, roughly
    movement_chance of sentences come from movement templates (as in the
    original app), regardless of how many templates each group has."""
    movement = [t for t in templates if "movement" in t.get("tags", [])]
    plain = [t for t in templates if "movement" not in t.get("tags", [])]
    use_movement = allow_movement and movement and rng.random() < movement_chance
    template = rng.choice(movement if use_movement else plain)
    return (template["id"], *fill_template(template, lexicon, rng))


if __name__ == "__main__":
    import sys

    templates, lexicon = load_templates(), load_lexicon()
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        for t in templates:
            print(f"{t['id']:40} {fill_template(t, lexicon)[0]}")
    else:
        n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
        for _ in range(n):
            tid, sentence, tree, _arrows = random_sentence(templates, lexicon, True)
            print(f"{tid:40} {sentence}")
