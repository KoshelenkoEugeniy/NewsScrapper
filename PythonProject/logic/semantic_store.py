import os
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

INDEX_DIR = "data_store/faiss_index"

def get_vector_store():
    if not os.path.exists(INDEX_DIR):
        return None

    try:
        return FAISS.load_local(INDEX_DIR, OpenAIEmbeddings(), allow_dangerous_deserialization=True)
    except ImportError as e:
        raise RuntimeError(f"FAISS not available: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Failed to load FAISS index: {e}") from e

def store_document(url, summary, topics, article_text):
    texts = [f"URL: {url}\n\nSummary:\n{summary}\n\nTopics:\n{', '.join(topics)}\n\nArticle:\n{article_text}"]
    metadata = [{"url": url, "summary": summary, "topics": topics, "article": article_text}]
    embeddings = OpenAIEmbeddings()

    vector_store = get_vector_store()
    if vector_store is None:
        vector_store = FAISS.from_texts(texts, embeddings, metadatas=metadata)
    else:
        vector_store.add_texts(texts, metadatas=metadata)

    vector_store.save_local(INDEX_DIR)

def semantic_search(query, k=3):
    vector_store = get_vector_store()
    if vector_store is None:
        return None
    return vector_store.similarity_search(query, k=k)

