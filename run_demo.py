from src.ontology_loader import OntologyLoader
from src.vectorstore_builder import build_vectorstore_if_needed
from src.retriever import get_context_for_aim
from src.rag_chain import generate_conversation

owl_path = "data/ontology/checkin.ttl"
aim = input("Nhập AIM: ").strip()
aim_name = aim[0].upper() + aim[1:]

# Parse ontology để lấy keyword/topic
loader = OntologyLoader(owl_path)
keywords = loader.get_keywords_for_aim(aim_name)
topic = loader.get_topic_for_aim(aim_name)

# Build vectorstore nếu chưa có
build_vectorstore_if_needed()

# Lấy context từ vectorstore
retrieved_context = get_context_for_aim(aim_name)

# Gộp prompt
context = f"Chủ đề: {topic}. Từ khóa: {', '.join(keywords)}. Nội dung gợi ý: {retrieved_context}"

# Gửi LLM
print(generate_conversation(context))
