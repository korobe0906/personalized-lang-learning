from src.ontology_reasoner import OntologyReasoner
from src.vectorstore_builder import load_or_build_vectorstore
from src.retriever import get_context_for_aim
from src.rag_chain import generate_conversation
from src.evaluator import evaluate_output
from src.student_memory import update_student_memory

# Đường dẫn OWL
owl_path = "data/ontology/aim_ontology.ttl"
reasoner = OntologyReasoner(owl_path)

# Build vectorstore nếu chưa có
load_or_build_vectorstore()

#  Cho nhập mã học viên ở đầu
student_id = input("Nhập mã học viên (vd: student_001): ").strip()

while True:
    print("\n==============================")
    aim = input("Nhập tên AIM (hoặc gõ 'exit' để thoát): ").strip()
    if aim.lower() == "exit":
        break

    aim_name = aim[0].upper() + aim[1:]

    # 1. Parse ontology để lấy thông tin AIM
    summary = reasoner.summarize_aim(aim_name)
    if not summary["keywords"]:
        print("AIM không tồn tại hoặc thiếu thông tin.")
        continue

    keywords = summary["keywords"]
    topic = summary.get("topic", "Unknown")

    # 2. Truy xuất context từ FAISS
    retrieved_context = get_context_for_aim(aim_name)

    # 3. In thông tin
    print(f"\n Chủ đề: {topic}")
    print(f" Từ khóa: {', '.join(keywords)}")
    print(f"\nNgữ cảnh tìm được:\n{retrieved_context}")

    # 4. Sinh hội thoại với LLM (gọi vào RAG + prompt)
    print("\n Hội thoại đề xuất:\n")
    conversation = generate_conversation(aim_name, reasoning=True)
    print(conversation)

    # 5. Tùy chọn đánh giá output
    choice = input("\n Bạn có muốn đánh giá hội thoại này không? (y/n): ").strip().lower()
    if choice == "y":
        result = evaluate_output(aim_name, conversation)
        print("\n Đánh giá kết quả:")
        print(f" Điểm khớp Ontology: {result['ontology_score']}")
        print(f" Điểm khớp RAG: {result['rag_score']}")
        print(f" Chấm theo Rubric: {result['rubric_score']}")
        print(f" Bloom Level: {result['bloom_level']}")
        print(f"\n Phản hồi của giáo viên:\n{result['feedback']}")

        #  Ghi log kết quả học
        update_student_memory(student_id, aim_name, result)
        print(f"Đã lưu kết quả học của {student_id} cho AIM {aim_name}.")
