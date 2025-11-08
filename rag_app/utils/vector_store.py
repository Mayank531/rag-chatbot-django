import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle
import os
from typing import List, Dict

class RAGVectorStore:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.metadata = []
        self.dimension = 384

    def build_from_chunks(self, chunks: List[tuple]):
        texts = [c[0] for c in chunks]
        embeddings = self.model.encode(texts)
        self.dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(np.array(embeddings).astype('float32'))
        self.metadata = [c[1] for c in chunks]  # page, type

    def save(self, index_path: str, meta_path: str):
        faiss.write_index(self.index, index_path)
        with open(meta_path, 'wb') as f:
            pickle.dump(self.metadata, f)

    def load(self, index_path: str, meta_path: str):
        self.index = faiss.read_index(index_path)
        with open(meta_path, 'rb') as f:
            self.metadata = pickle.load(f)

    def retrieve(self, query: str, k: int = 3) -> List[Dict]:
        q_emb = self.model.encode([query])
        D, I = self.index.search(np.array(q_emb).astype('float32'), k)
        results = []
        for idx in I[0]:
            if idx < len(self.metadata):
                results.append({
                    "text": "",  # not stored, but we return metadata
                    "metadata": self.metadata[idx]
                })
        return results