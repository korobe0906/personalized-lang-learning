

def build_prompt(topic: str, keywords: list[str], context: str) -> str:

    keywords_str = ", ".join(keywords) if keywords else "none"

    prompt = f"""
Bạn là giáo viên tiếng Anh giao tiếp. Hãy viết một đoạn hội thoại đơn giản theo yêu cầu dưới đây.

    Mục tiêu học: {topic}
    Từ khóa cần sử dụng: {keywords_str}
    Ngữ cảnh tham khảo:
{context}

Yêu cầu:
- Hội thoại không quá 5 câu
- Ngắn gọn, rõ ràng, cấp độ sơ cấp (A1 – A2)
- Ưu tiên tình huống thực tế, sinh động
- Chỉ viết đoạn hội thoại, không chú thích

==> Hội thoại:
""".strip()

    return prompt

