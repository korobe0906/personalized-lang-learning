from src.ontology_loader import OntologyLoader
import os

owl_path = "data/ontology/checkin.ttl"
output_path = "data/output/corpus.txt"

loader = OntologyLoader(owl_path)
aims = loader.get_all_aims()

os.makedirs(os.path.dirname(output_path), exist_ok=True)  # 🔧 Fix lỗi

with open(output_path, "w", encoding="utf-8") as f:
    for aim in aims:
        topic = loader.get_topic_for_aim(aim)
        keywords = loader.get_keywords_for_aim(aim)
        f.write(f"{aim}AIM: Chủ đề là {topic}. Từ khóa: {', '.join(keywords)}.\n")
