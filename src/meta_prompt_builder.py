from src.student_memory import load_student_memory


def build_prompt_with_memory(topic: str, keywords: list[str], context: str) -> str:
    memory = load_student_memory()

    old_keywords = ", ".join(memory.get("learned_keywords", []))
    common_errors = ", ".join(memory.get("common_errors", []))
    last_feedback = ", ".join(memory.get("last_feedback", []))
    level = ", ".join(memory.get("level", []))

    keywords_str = ", ".join(keywords)

    prompt = f"""
Bạn là giáo viên cá nhân hóa. Dưới đây là hồ sơ học sinh:

- Trình độ: {level}
- AIM hiện tại: {topic}
- Từ khóa đã học: {old_keywords}
- Từ khóa mới: {keywords_str}
- Lỗi thường gặp: {common_errors}
- Ghi chú gần nhất: {last_feedback}

Ngữ cảnh: {context}

Nhiệm vụ:
- Viết hội thoại dưới 5 câu, đơn giản, rõ ràng.
- Dùng từ khóa mới, lặp lại ít nhất 1 từ khóa cũ.
- Tránh lỗi học sinh thường gặp.
- Có cảm xúc, gần gũi thực tế.

==> Hội thoại:
""".strip()
    return prompt
