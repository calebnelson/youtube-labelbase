from pytube import YouTube
from typing import Dict, Any

def get_video_metadata(url: str) -> Dict[str, Any]:
    """
    Get video metadata from YouTube.
    """
    try:
        yt = YouTube(url)
        return {
            "title": yt.title,
            "channel": yt.author,
            "duration": str(yt.length),
            "description": yt.description,
            "views": yt.views,
            "publish_date": yt.publish_date.isoformat() if yt.publish_date else None,
            "keywords": yt.keywords,
            "thumbnail_url": yt.thumbnail_url,
        }
    except Exception as e:
        raise Exception(f"Error fetching video metadata: {str(e)}")

def get_video_transcript(url: str) -> str:
    """
    Get video transcript from YouTube.
    """
    try:
        yt = YouTube(url)
        # Note: This is a placeholder. You'll need to implement actual transcript fetching
        # using youtube_transcript_api or similar
        return ""
    except Exception as e:
        raise Exception(f"Error fetching video transcript: {str(e)}") 