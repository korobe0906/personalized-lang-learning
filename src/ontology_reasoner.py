
from rdflib import Graph, Namespace, RDF, RDFS, OWL
from owlrl import DeductiveClosure, OWLRL_Semantics

class OntologyReasoner:
    def __init__(self, ttl_path):
        self.graph = Graph()
        self.graph.parse(ttl_path, format="ttl")
        DeductiveClosure(OWLRL_Semantics).expand(self.graph)

        self.ns = Namespace("http://example.org/lang-learning#")

    def get_keywords(self, aim_uri):
        return [str(o).split("#")[-1] for o in self.graph.objects(aim_uri, self.ns.hasKeyword)]

    def get_topic(self, aim_uri):
        topics = [str(o).split("#")[-1] for o in self.graph.objects(aim_uri, self.ns.hasTopic)]
        return topics[0] if topics else None

    def get_prerequisites(self, aim_uri):
        return [str(o).split("#")[-1] for o in self.graph.objects(aim_uri, self.ns.preRequisite)]

    def get_related(self, aim_uri):
        return [str(o).split("#")[-1] for o in self.graph.objects(aim_uri, self.ns.relatedTo)]

    def get_equivalent_aims(self, aim_uri):
        return [str(s).split("#")[-1] for s in self.graph.subjects(OWL.equivalentClass, aim_uri)] + \
               [str(o).split("#")[-1] for o in self.graph.objects(aim_uri, OWL.equivalentClass)]

    def get_subclasses(self, aim_uri):
        return [str(s).split("#")[-1] for s in self.graph.subjects(RDFS.subClassOf, aim_uri)]

    def get_intersections(self):
        results = []
        for s, p, o in self.graph.triples((None, OWL.intersectionOf, None)):
            results.append(str(s).split("#")[-1])
        return results

    def get_transitive_topics(self):
        topics = set()
        for s, _, o in self.graph.triples((None, self.ns.hasParentTopic, None)):
            topics.add((str(s).split("#")[-1], str(o).split("#")[-1]))
        return list(topics)

    def summarize_aim(self, aim_id, include_reasoning=False):
        aim_uri = self.ns[aim_id]

        if include_reasoning:
            summary = {
                "equivalent_aims": self.get_equivalent_aims(aim_id),
                "related_aims": self.get_related(aim_id),
            }
        else:
            summary = {
                "equivalent_aims": [],
                "related_aims": [],
            }

        summary.update({
            "aim": aim_id,
            "keywords": self.get_keywords(aim_uri),
            "topic": self.get_topic(aim_uri),
            "prerequisites": self.get_prerequisites(aim_uri),
        })

        return summary
