from sentence_transformers import util

class VideoSearch:
    def __init__(self, embedder, video_embeddings, videos):
        self.embedder = embedder
        self.video_embeddings = video_embeddings
        self.videos = videos

    def search(self, query, top_k=5):
        query_embedding = self.embedder.embed_query(query)

        scores = util.cos_sim(query_embedding, self.video_embeddings)[0]

        print("Number of videos:", len(self.videos))

        k = min(top_k, len(self.videos))
        top_results = scores.topk(k=k)


        results = []

        for score, idx in zip(top_results.values, top_results.indices):
            results.append({
                "title": self.videos[idx]["title"],
                "url": self.videos[idx]["url"],
                "score": score.item()
            })

        return results
