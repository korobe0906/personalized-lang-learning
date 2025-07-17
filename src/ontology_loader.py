from rdflib import Graph, Namespace, RDFS

class OntologyLoader:
    def __init__(self, path):
        self.graph = Graph()
        self.graph.parse(path, format="turtle")
        self.ns = Namespace("http://example.org/lang-learning#")

    def get_keywords_for_aim(self, aim_name):
        aim_uri = self.ns[f"{aim_name}AIM"]
        print(f"AIM URI (keyword): {aim_uri}")
        q = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?label
        WHERE {{
            <{aim_uri}> <{self.ns['hasKeyword']}> ?kw .
            ?kw rdfs:label ?label .
        }}
        """
        print("SPARQL query:\n", q)
        results = self.graph.query(q)
        return [str(row.label) for row in results]

    def get_topic_for_aim(self, aim_name):
        aim_uri = self.ns[f"{aim_name}AIM"]
        print(f"AIM URI (topic): {aim_uri}")
        q = f"""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        SELECT ?label
        WHERE {{
            <{aim_uri}> <{self.ns['hasTopic']}> ?topic .
            ?topic rdfs:label ?label .
        }}
        """
        print("SPARQL query:\n", q)
        results = self.graph.query(q)
        for row in results:
            return str(row.label)
        return None

    def get_all_aims(self):
        q = f"""
        SELECT ?aim
        WHERE {{
            ?aim a <{self.ns['AIM']}> .
        }}
        """
        results = self.graph.query(q)
        return [str(row.aim).split("#")[-1].replace("AIM", "") for row in results]