from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from rdflib import Graph, Namespace, RDF, RDFS, OWL
import os

ONTOLOGY_PATH = "data/ontology/aim_ontology.ttl"
INDEX_PATH = "data/output/faiss_index"

def get_all_related_aims(graph: Graph, ns, aim_uri):
    """
    Truy xuất các AIM liên quan:
    - AIM tương đương (owl:equivalentClass)
    - AIM tích hợp (owl:intersectionOf)
    - AIM tiền đề (preRequisite)
    """
    related_aims = set()
    related_aims.add(aim_uri)

    # 1. Truy ra AIM tương đương (equivalentClass)
    for s in graph.subjects(OWL.equivalentClass, aim_uri):
        related_aims.add(s)
    for o in graph.objects(aim_uri, OWL.equivalentClass):
        related_aims.add(o)

    # 2. Truy ra AIM tích hợp (intersectionOf)
    for s in graph.subjects(OWL.intersectionOf, None):
        items = graph.value(subject=s, predicate=OWL.intersectionOf)
        if items:
            for item in items:
                if isinstance(item, list) and aim_uri in item:
                    related_aims.add(s)

    # 3. Truy ra AIM tiền đề (preRequisite)
    for s in graph.subjects(ns.preRequisite, aim_uri):
        related_aims.add(s)
    for o in graph.objects(aim_uri, ns.preRequisite):
        related_aims.add(o)

    return list(related_aims)

def get_keywords_for_aims(graph: Graph, ns, aim_uris):
    keywords = set()
    for aim_uri in aim_uris:
        for kw in graph.objects(subject=aim_uri, predicate=ns.hasKeyword):
            label = graph.value(subject=kw, predicate=RDFS.label)
            if label:
                keywords.add(str(label))
    return list(keywords)

def get_context_for_aim(aim_name: str, use_reasoning: bool = True) -> str:
    # Load ontology
    g = Graph()
    g.parse(ONTOLOGY_PATH, format="turtle")
    ns = Namespace("http://example.org/lang-learning#")
    aim_uri = ns[aim_name]

    print(" AIM URI:", aim_uri)

    if use_reasoning:
        related_aims = get_all_related_aims(g, ns, aim_uri)
        print(" Reasoning bật - AIM liên quan:", [str(uri).split("#")[-1] for uri in related_aims])
    else:
        related_aims = [aim_uri]
        print("⚡ Reasoning tắt - chỉ dùng AIM hiện tại.")

    keywords = get_keywords_for_aims(g, ns, related_aims)
    if not keywords:
        print(" Không tìm thấy keyword.")
        return ""

    print(" Từ khóa dùng để truy vấn FAISS:", keywords)

    # Load FAISS vectorstore
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.load_local(INDEX_PATH, embeddings=embeddings, allow_dangerous_deserialization=True)

    retrieved_docs = db.similarity_search(" ".join(keywords), k=4)
    context = "\n".join([doc.page_content for doc in retrieved_docs])

    return context
