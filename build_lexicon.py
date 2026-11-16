"""Build lexicon.json from words.txt, generating plurals and verb forms.

    python build_lexicon.py            # write lexicon.json
    python build_lexicon.py --review   # also print every generated form

Requires lemminflect (dev only: pip install -r requirements-dev.txt).
The app itself only reads lexicon.json.
"""
import json
import sys

from lemminflect import getInflection

from madlib import VERB_FRAMES

SRC, OUT = "words.txt", "lexicon.json"
VERB_TAGS = {"3sg": "VBZ", "past": "VBD", "prog": "VBG"}


def parse(path):
    sections, current = {}, None
    for n, raw in enumerate(open(path, encoding="utf-8"), 1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if line.startswith("[") and line.endswith("]"):
            current = sections.setdefault(line[1:-1], [])
            continue
        if current is None:
            sys.exit(f"{path}:{n}: word before any [section]")
        main, _, extra = line.partition("|")
        overrides = dict(kv.split("=", 1) for kv in extra.split())
        current.append((n, main.strip(), overrides))
    return sections


def inflect(word, tag, n):
    forms = getInflection(word, tag)
    if not forms:
        sys.exit(f"{SRC}:{n}: no {tag} form for '{word}'; add an override")
    return forms[0]


def build(sections):
    lexicon, problems = {}, []
    for name, entries in sections.items():
        seen = set()
        for n, main, _ in entries:
            key = main.split(":")[0].strip()
            if key in seen:
                problems.append(f"{SRC}:{n}: duplicate '{key}' in [{name}]")
            seen.add(key)

        if name == "noun":
            lexicon["noun"] = [
                [w, ov.get("pl") or inflect(w, "NNS", n)] for n, w, ov in entries
            ]
        elif name == "verb":
            verbs = []
            for n, main, ov in entries:
                base, _, frames = main.partition(":")
                base, frames = base.strip(), frames.split()
                bad = [f for f in frames if f not in VERB_FRAMES]
                if not frames or bad:
                    problems.append(f"{SRC}:{n}: '{base}' needs frames from {VERB_FRAMES}")
                entry = {"base": base}
                for form, tag in VERB_TAGS.items():
                    entry[form] = ov.get(form) or inflect(base, tag, n)
                entry["frames"] = frames
                verbs.append(entry)
            lexicon["verb"] = verbs
        else:
            lexicon[name] = [w for _, w, _ in entries]

    for frame in VERB_FRAMES:
        if not any(frame in v["frames"] for v in lexicon.get("verb", [])):
            problems.append(f"no verbs with frame '{frame}'")
    return lexicon, problems


def dump(lexicon):
    """One entry per line, so git diffs of lexicon.json stay readable."""
    parts = []
    for name, entries in lexicon.items():
        body = ",\n".join("    " + json.dumps(e, ensure_ascii=False) for e in entries)
        parts.append(f'  {json.dumps(name)}: [\n{body}\n  ]')
    return "{\n" + ",\n".join(parts) + "\n}\n"


if __name__ == "__main__":
    lexicon, problems = build(parse(SRC))
    if problems:
        sys.exit("\n".join(problems))
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(dump(lexicon))
    print(", ".join(f"{len(v)} {k}" for k, v in lexicon.items()))
    if "--review" in sys.argv:
        for sg, pl in lexicon["noun"]:
            print(f"  {sg:15} {pl}")
        for v in lexicon["verb"]:
            print(f"  {v['base']:15} {v['3sg']:15} {v['past']:15} {v['prog']:15} {' '.join(v['frames'])}")
