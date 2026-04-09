import os
import json
from ai.embedder import Embedder
from ai.search import VideoSearch
from ai.youtube_fetcher import get_channel_id_from_url, get_videos

DATA_PATH = "data/videos.json"
EMBED_PATH = "data/embeddings.pkl"


def fetch_and_cache_videos(channel_id):
    """
    Fetch videos from YouTube and store locally
    """
    print("Fetching videos from YouTube...")
    videos = get_videos(channel_id)

    with open(DATA_PATH, "w") as f:
        json.dump(videos, f, indent=2)

    print(f"Saved {len(videos)} videos locally.")
    return videos


def load_cached_videos():
    """
    Load videos from local storage
    """
    if not os.path.exists(DATA_PATH):
        return []

    with open(DATA_PATH, "r") as f:
        return json.load(f)


def main():
    channel_url = "https://www.youtube.com/@joerogan"  # 🔥 PUT YOUR CHANNEL URL HERE

    channel_id = get_channel_id_from_url(channel_url)

    embedder = Embedder()

    # Step 1 — Load cached videos
    videos = load_cached_videos()

    # Step 2 — If no videos, fetch from YouTube
    if not videos:
        videos = fetch_and_cache_videos(channel_id)

    # Step 3 — Generate or load embeddings
    if not os.path.exists(EMBED_PATH):
        print("Creating embeddings...")
        video_embeddings = embedder.embed_videos(videos)
        embedder.save_embeddings(video_embeddings, EMBED_PATH)
        print("Embeddings saved.")
    else:
        print("Loading embeddings...")
        video_embeddings = embedder.load_embeddings(EMBED_PATH)

    # Step 4 — Initialize search
    search_engine = VideoSearch(embedder, video_embeddings, videos)

    print("\n=== YouTube AI Video Search ===")

    # Step 5 — Interactive search
    while True:
        query = input("\nEnter genre/search query (or 'exit'): ")

        if query.lower() == "exit":
            break

        results = search_engine.search(query, top_k=10)

        print("\nResults:\n")

        for r in results:
            print(f"{r['title']}")
            print(f"Score: {r['score']:.4f}")
            print(f"URL: {r['url']}")
            print("-" * 50)


if __name__ == "__main__":
    main()
