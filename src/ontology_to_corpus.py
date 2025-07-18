# ontology_to_corpus.py
from rdflib import Graph, Namespace, RDFS
import os

AIM = Namespace("http://example.org/lang-learning#")

def extract_triples_from_ontology(ttl_path: str, output_path: str):
    g = Graph()
    g.parse(ttl_path, format="turtle")

    aim_classes = list(g.subjects(RDFS.label, None))
    content_lines = []

    for aim_uri in aim_classes:
        label = g.value(aim_uri, RDFS.label)
        if label is None or not str(aim_uri).endswith("AIM"):
            continue

        aim_name = str(label)
        lines = [f"AIM: {aim_name}"]

        # Topic
        for topic in g.objects(aim_uri, AIM.hasTopic):
            topic_label = g.value(topic, RDFS.label)
            if topic_label:
                lines.append(f"Topic: {topic_label}")

        # Keywords
        for kw in g.objects(aim_uri, AIM.hasKeyword):
            kw_label = g.value(kw, RDFS.label)
            if kw_label:
                lines.append(f"Keyword: {kw_label}")

        # Prerequisite
        for pre in g.objects(aim_uri, AIM.preRequisite):
            pre_label = g.value(pre, RDFS.label)
            if pre_label:
                lines.append(f"Prerequisite: {pre_label}")

        # Related
        for related in g.objects(aim_uri, AIM.relatedTo):
            rel_label = g.value(related, RDFS.label)
            if rel_label:
                lines.append(f"Related: {rel_label}")

        # Tích hợp owl:intersectionOf
        for combo in g.subjects(predicate=RDFS.label, object=label):
            for lst in g.objects(combo, AIM.hasTopic):
                lines.append(f"Integrated Topic: {g.value(lst, RDFS.label)}")

        content_lines.append("\n".join(lines))
        content_lines.append("")

    # Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(content_lines))
    print(f"Corpus saved to {output_path}")

# Example usage:
if __name__ == "__main__":
    extract_triples_from_ontology(
        ttl_path="data/ontology/aim_ontology.ttl",
        output_path="data/output/corpus.txt"
    )
