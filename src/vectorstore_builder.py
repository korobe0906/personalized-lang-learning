import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def build_vectorstore_if_needed(corpus_path="data/output/corpus.txt", save_path="data/output/faiss_index"):
    # In debug để kiểm tra đường dẫn
    print(f"Đang kiểm tra file corpus tại: {corpus_path}")

    # Nếu file không tồn tại thì báo lỗi rõ ràng
    if not os.path.exists(corpus_path):
        raise FileNotFoundError(f"Không tìm thấy file corpus: {corpus_path}")

    #Nếu vectorstore đã có rồi thì load
    if os.path.exists(save_path + ".faiss"):
        print("Đã tồn tại FAISS index, đang load...")
        return FAISS.load_local(save_path, HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"))

    # Load dữ liệu
    loader = TextLoader(corpus_path, encoding="utf-8")  # ✅ thêm encoding
    documents = loader.load()

    # Tách đoạn
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    docs = splitter.split_documents(documents)

    # Tạo vectorstore
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = FAISS.from_documents(docs, embeddings)

    # Lưu lại
    vectordb.save_local(save_path)
    print(f"Đã tạo và lưu FAISS vectorstore tại {save_path}")
    return vectordb
