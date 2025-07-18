from src.ontology_reasoner import OntologyReasoner
from src.retriever import get_context_for_aim


from difflib import SequenceMatcher
from src.grok_client import call_grok_llm
from src.student_memory import update_student_memory, load_student_memory


### 3. Kiểm tra alignment với Ontology
def check_with_ontology(output: str, summary: dict) -> float:
    keywords = summary.get("keywords", [])
    matched = [kw for kw in keywords if kw.lower() in output.lower()]
    if not keywords:
        return 0.5
    return round(len(matched) / len(keywords), 2)


### 4. Kiểm tra RAG context match
def check_with_rag(output: str, context: str) -> float:
    def similarity(a, b):
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()

    if not context:
        return 0.0
    return round(similarity(output, context), 2)


### 5. Rubric scoring
def score_by_rubric(output: str, summary: dict) -> dict:
    score = {"contextual": 0, "keywords": 0, "simplicity": 0}

    # 1. Đúng ngữ cảnh (ví dụ chứa topic)
    if summary.get("topic", "").lower() in output.lower():
        score["contextual"] = 2

    # 2. Đủ từ khóa (>= 60% keywords)
    kws = summary.get("keywords", [])
    matched = [k for k in kws if k.lower() in output.lower()]
    if len(kws) > 0:
        ratio = len(matched) / len(kws)
        if ratio >= 0.6:
            score["keywords"] = 2
        elif ratio >= 0.3:
            score["keywords"] = 1

    # 3. Ngắn gọn và đơn giản (A1–A2)
    if len(output.split()) <= 60:
        score["simplicity"] = 2
    elif len(output.split()) <= 100:
        score["simplicity"] = 1

    return score


### 6. Phân loại theo Bloom

def classify_bloom_level(output: str) -> str:
    prompt = f"""
Given the following text:
"{output}"

Classify it into one level of Bloom's Taxonomy:
1. Remember
2. Understand
3. Apply
4. Analyze
5. Evaluate
6. Create

Explain your reasoning and output only the level name.
"""
    result = call_grok_llm(prompt)
    return result.strip()


### 7. Tạo phản hồi bằng LLM
def generate_feedback(output: str, summary: dict, rubric_score: dict, bloom_level: str) -> str:
    keywords = ", ".join(summary.get("keywords", []))
    topic = summary.get("topic", "unknown")

    prompt = f"""
You are an English teacher evaluating a student's conversation:
"{output}"

Topic: {topic}
Required keywords: {keywords}
Bloom level: {bloom_level}
Rubric score: {rubric_score}

Write a short feedback:
- What is good?
- What could be improved?
- Suggestions to improve it.
"""
    return call_grok_llm(prompt).strip()
def evaluate_output(aim_name: str, user_output: str) -> dict:
    """
    Đánh giá đầu ra do LLM sinh dựa trên AIM yêu cầu.
    """
    # 1. Lấy dữ liệu từ ontology (keywords, topic, level)
    summary = OntologyReasoner("data/ontology/aim_ontology.ttl").summarize_aim(aim_name)

    # 2. Truy xuất nội dung chuẩn từ FAISS
    context = get_context_for_aim(aim_name)

    # 3. Kiểm tra alignment từ output với ontology
    ontology_score = check_with_ontology(user_output, summary)

    # 4. Kiểm tra nội dung có khớp với tài liệu không (RAG)
    rag_score = check_with_rag(user_output, context)

    # 5. Chấm điểm theo rubric
    rubric_score = score_by_rubric(user_output, summary)

    # 6. Xác định Bloom level
    bloom_level = classify_bloom_level(user_output)

    # 7. Phản hồi tổng hợp từ LLM
    feedback = generate_feedback(user_output, summary, rubric_score, bloom_level)

    return {
        "ontology_score": ontology_score,
        "rag_score": rag_score,
        "rubric_score": rubric_score,
        "bloom_level": bloom_level,
        "feedback": feedback,
        "total_score": round((ontology_score + rag_score + sum(rubric_score.values()) / 6) / 3, 2)
    }
def log_learning_result(aim_name, rubric_score, ontology_score, rag_score, bloom_level, feedback):
    memory = load_student_memory()

    if "progress" not in memory:
        memory["progress"] = {}

    if aim_name not in memory["progress"]:
        memory["progress"][aim_name] = {
            "attempts": 0,
            "last_score": {}
        }

    memory["progress"][aim_name]["attempts"] += 1
    memory["progress"][aim_name]["last_score"] = {
        "rubric": rubric_score,
        "ontology": ontology_score,
        "rag": rag_score,
        "bloom": bloom_level
    }

    memory["last_feedback"] = feedback.strip()

    update_student_memory(memory)
