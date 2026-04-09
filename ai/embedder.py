from sentence_transformers import SentenceTransformer
import pickle

class Embedder:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def prepare_text(self, video):
        return f"{video['title']}. {video['description']}"

    def embed_videos(self, videos):
        texts = [self.prepare_text(v) for v in videos]
        embeddings = self.model.encode(texts, convert_to_tensor=True)
        return embeddings

    def embed_query(self, query):
        return self.model.encode(query, convert_to_tensor=True)

    def save_embeddings(self, embeddings, path):
        with open(path, "wb") as f:
            pickle.dump(embeddings, f)

    def load_embeddings(self, path):
        with open(path, "rb") as f:
            return pickle.load(f)
