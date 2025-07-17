from rdflib import Graph, Namespace, RDF, RDFS, OWL, URIRef, Literal
from owlrl import DeductiveClosure, OWLRL_Semantics

# Load ontology
g = Graph()
g.parse("data/ontology/aim_ontology.ttl", format="turtle")

# Reasoning
DeductiveClosure(OWLRL_Semantics).expand(g)
print("OWL reasoning applied.\n")

EX = Namespace("http://example.org/lang-learning#")

# --- 1. equivalentClass ---
print("Equivalent AIMs (owl:equivalentClass):")
for s, p, o in g.triples((None, OWL.equivalentClass, None)):
    print(f" - {s.split('#')[-1]} <=> {o.split('#')[-1]}")
print()

# --- 2. intersectionOf ---
print("AIMs with Integrated Topics (owl:intersectionOf):")
for s, p, o in g.triples((None, OWL.intersectionOf, None)):
    print(f" - {s.split('#')[-1]} integrates: {o}")
print()

# --- 3. unionOf ---
print("AIMs with Extended Classification (owl:unionOf):")
for s, p, o in g.triples((None, OWL.unionOf, None)):
    print(f" - {s.split('#')[-1]} covers either of: {o}")
print()

# --- 4. hasValue / allValuesFrom ---
print("AIMs with keyword/topic constraints (owl:hasValue / allValuesFrom):")
for restriction in g.subjects(RDF.type, OWL.Restriction):
    on_prop = g.value(restriction, OWL.onProperty)
    val = g.value(restriction, OWL.hasValue) or g.value(restriction, OWL.allValuesFrom)
    for class_ in g.subjects(RDFS.subClassOf, restriction):
        print(f" - {class_.split('#')[-1]} has constraint: {on_prop.split('#')[-1]} = {val.split('#')[-1]}")
print()

# --- 5. transitiveProperty ---
print("Topics with Transitive Parent (owl:TransitiveProperty):")
for s, _, p1 in g.triples((None, EX.hasParentTopic, None)):
    for _, _, p2 in g.triples((p1, EX.hasParentTopic, None)):
        print(f" - {s.split('#')[-1]} => {p1.split('#')[-1]} => {p2.split('#')[-1]}")
print()

# --- 6. subClassOf ---
print("AIM Subclasses (rdfs:subClassOf):")
for s, _, o in g.triples((None, RDFS.subClassOf, None)):
    print(f" - {s.split('#')[-1]} ⊆ {o.split('#')[-1]}")
