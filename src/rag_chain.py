# rag_chain.py

from src.vectorstore_builder import build_vectorstore_from_ontology
from src.ontology_reasoner import OntologyReasoner
from src.meta_prompt_builder import build_prompt_with_memory
from src.grok_client import call_grok_llm
from src.vectorstore_builder import load_or_build_vectorstore
# Khởi tạo reasoner từ OWL ontology
reasoner = OntologyReasoner("data/ontology/aim_ontology.ttl")


def generate_conversation(aim_name: str, reasoning: bool = True) -> str:
    # 1. Lấy thông tin từ ontology
    summary = reasoner.summarize_aim(aim_name, include_reasoning=reasoning)
    keywords = summary["keywords"]
    topic = summary["topic"]
    prerequisites = summary["prerequisites"]
    equivalents = summary["equivalent_aims"]
    related = summary["related_aims"]

    # Gộp các term cần dùng để truy vấn
    search_terms = keywords + [topic] + prerequisites + equivalents + related
    if not search_terms:
        return f" Không tìm thấy ngữ cảnh phù hợp cho AIM: {aim_name}"

    # 2. Build hoặc load FAISS vectorstore
    vectordb = load_or_build_vectorstore()

    # 3. Truy vấn context từ FAISS
    search_query = ", ".join(search_terms)
    docs = vectordb.similarity_search(search_query, k=5)
    context = "\n".join([doc.page_content for doc in docs])

    if not context:
        return f" Không tìm thấy tài liệu phù hợp với: {search_query}"

    # 4. Build prompt đúng cách
    prompt = build_prompt_with_memory(topic=topic, keywords=keywords, context=context)

    # 5. Gọi Groq LLM để sinh hội thoại
    return call_grok_llm(prompt)

