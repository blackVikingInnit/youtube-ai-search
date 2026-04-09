import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")


def get_videos(channel_id):
    print("Getting uploads playlist...")
    playlist_id = get_uploads_playlist_id(channel_id)

    print("Fetching all videos from playlist...")
    videos = get_all_videos_from_playlist(playlist_id)

    print(f"Total videos fetched: {len(videos)}")

    return videos


def extract_handle_from_url(url):
    if "@" in url:
        return url.split("@")[-1].split("/")[0]
    return None


def get_channel_id_from_handle(handle):
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&type=channel&q={handle}&key={API_KEY}"

    print("API KEY: ", API_KEY)  # DEBUG

    res = requests.get(url, timeout=10)

    if res.status_code != 200:
        print(res.text)  # DEBUG
        raise Exception(f"API request failed: {res.status_code}")

    data = res.json()

    items = data.get("items", [])
    if not items:
        return None

    return items[0]["snippet"]["channelId"]


def get_channel_id_from_url(url):
    handle = extract_handle_from_url(url)

    if not handle:
        raise ValueError(f"Invalid YouTube URL: {url}")

    channel_id = get_channel_id_from_handle(handle)

    if not channel_id:
        raise ValueError("Channel not found")

    return channel_id


def get_uploads_playlist_id(channel_id):
    url = f"https://www.googleapis.com/youtube/v3/channels?part=contentDetails&id={channel_id}&key={API_KEY}"

    res = requests.get(url, timeout=10)

    if res.status_code != 200:
        raise Exception(f"API request failed: {res.status_code}")

    data = res.json()

    return data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

def get_all_videos_from_playlist(playlist_id):
    url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={playlist_id}&maxResults=50&key={API_KEY}"

    videos = []

    while url:
        res = requests.get(url, timeout=10)

        if res.status_code != 200:
            raise Exception(f"API request failed: {res.status_code}")

        data = res.json()

        for item in data.get("items", []):
            snippet = item["snippet"]

            videos.append({
                "title": snippet["title"],
                "description": snippet["description"],
                "url": f"https://youtube.com/watch?v={snippet['resourceId']['videoId']}"
            })

        next_page = data.get("nextPageToken")

        if next_page:
            url = f"https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={playlist_id}&maxResults=50&pageToken={next_page}&key={API_KEY}"
        else:
            break

    return videos
