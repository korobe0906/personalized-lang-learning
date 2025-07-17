

from src.groq_client import call_groq_llm

def generate_conversation(context):
    prompt = f"""Bạn là giáo viên tiếng Anh. Dựa trên ngữ cảnh dưới đây, viết đoạn hội thoại tiếng Anh đơn giản.

Ngữ cảnh:
{context}

Yêu cầu:
- Cấp độ: sơ cấp
- Dài: ≤ 5 câu
- Thực tế, dễ hiểu

==> Hội thoại:
"""
    return call_groq_llm(prompt)


