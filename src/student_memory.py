import json
import os
from pathlib import Path

MEMORY_PATH = Path("data/output/student_memory.json")

def load_student_memory():
    with open(MEMORY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def update_student_memory(student_id, aim_name, result, filepath="data/output/student_memory.json"):
    if not os.path.exists(filepath):
        memory = {}
    else:
        with open(filepath, "r", encoding="utf-8") as f:
            memory = json.load(f)

    if student_id not in memory:
        memory[student_id] = []

    memory[student_id].append({
        "aim": aim_name,
        "ontology_score": result.get("ontology_score", 0),
        "rag_score": result.get("rag_score", 0),
        "rubric_score": result.get("rubric_score", {}),
        "bloom_level": result.get("bloom_level", ""),
        "feedback": result.get("feedback", "")
    })

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2, ensure_ascii=False)
