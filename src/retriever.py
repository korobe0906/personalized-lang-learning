from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def get_context_for_aim(aim_name, index_path="data/output/faiss_index"):
    # Load vectorstore FAISS đã lưu
    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.load_local(index_path, embeddings=embedding, allow_dangerous_deserialization=True)


    # Truy vấn context theo tên AIM (dạng 'CheckInAIM')
    docs = db.similarity_search(aim_name, k=2)  # lấy 2 đoạn gần nhất
    return "\n".join([doc.page_content for doc in docs])
