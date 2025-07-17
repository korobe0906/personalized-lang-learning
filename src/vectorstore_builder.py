# vectorstore_builder.py
import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

from src.ontology_to_corpus import extract_triples_from_ontology

def build_vectorstore_from_ontology(
    ontology_path: str = "data/ontology/aim_ontology.ttl",
    corpus_path: str = "data/output/corpus.txt",
    index_path: str = "data/output/faiss_index"
):
    print(f"Đang kiểm tra file corpus tại: {corpus_path}")

    # Bước 1: Chuyển ontology thành corpus
    extract_triples_from_ontology(ontology_path, corpus_path)

    # Bước 2: Load corpus thành documents
    loader = TextLoader(corpus_path, encoding="utf-8")
    docs = loader.load()
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = splitter.split_documents(docs)

    # Bước 3: Embedding + FAISS
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(split_docs, embeddings)

    # Bước 4: Lưu index
    os.makedirs(index_path, exist_ok=True)
    vectorstore.save_local(index_path)
    print(f"Đã tạo và lưu FAISS vectorstore tại {index_path}")

if __name__ == "__main__":
    build_vectorstore_from_ontology()
