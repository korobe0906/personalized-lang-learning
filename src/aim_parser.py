import json

def load_ontology(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def parse_aim(aim_text, ontology):
    matched = []
    for topic, keywords in ontology.items():
        if any(word in aim_text.lower() for word in keywords + [topic]):
            matched.append(topic)
    return matched or ["general"]