from googleapiclient.discovery import build
from typing import Dict, Any
import re
import time
from urllib.parse import urlparse, parse_qs
import logging
import os
from datetime import datetime
from app.core.config import settings
logger = logging.getLogger(__name__)

def extract_video_id(url: str) -> str:
    """
    Extract video ID from various YouTube URL formats.
    """
    # Handle youtu.be URLs
    if "youtu.be" in url:
        return url.split("/")[-1].split("?")[0]
    
    # Handle youtube.com URLs
    parsed_url = urlparse(url)
    if parsed_url.netloc in ["www.youtube.com", "youtube.com"]:
        if parsed_url.path == "/watch":
            return parse_qs(parsed_url.query)["v"][0]
        elif parsed_url.path.startswith(("/embed/", "/v/")):
            return parsed_url.path.split("/")[2]
    
    raise ValueError("Invalid YouTube URL format")

def get_video_metadata(url: str, api_key: str = None, max_retries: int = 3) -> Dict[str, Any]:
    """
    Get video metadata from YouTube using the YouTube Data API.
    
    Args:
        url: YouTube video URL
        api_key: YouTube Data API key (can be set via YOUTUBE_API_KEY environment variable)
        max_retries: Maximum number of retry attempts
        
    Returns:
        Dict containing video metadata
        
    Raises:
        ValueError: If URL is invalid or API key is missing
        Exception: If metadata cannot be fetched after retries
    """
    # Use API key from arguments or environment variable
    api_key = api_key or settings.YOUTUBE_API_KEY
    if not api_key:
        raise ValueError("YouTube API key is required. Set it as an argument or YOUTUBE_API_KEY environment variable.")
    
    video_id = extract_video_id(url)
    
    for attempt in range(max_retries):
        try:
            # Build the YouTube API client
            youtube = build('youtube', 'v3', developerKey=api_key)
            
            # Get video details
            video_response = youtube.videos().list(
                part="snippet,contentDetails,statistics,status",
                id=video_id
            ).execute()
            
            if not video_response.get('items'):
                raise ValueError(f"Video {video_id} not found or not accessible")
            
            video_data = video_response['items'][0]
            snippet = video_data['snippet']
            statistics = video_data['statistics']
            content_details = video_data['contentDetails']
            status = video_data['status']
            
            # Parse duration (ISO 8601 format)
            duration_str = content_details['duration']
            # Convert PT1H2M3S format to seconds
            duration_seconds = 0
            hours_match = re.search(r'(\d+)H', duration_str)
            minutes_match = re.search(r'(\d+)M', duration_str)
            seconds_match = re.search(r'(\d+)S', duration_str)
            
            if hours_match:
                duration_seconds += int(hours_match.group(1)) * 3600
            if minutes_match:
                duration_seconds += int(minutes_match.group(1)) * 60
            if seconds_match:
                duration_seconds += int(seconds_match.group(1))
            
            # Format publish date
            publish_date = None
            if snippet.get('publishedAt'):
                publish_date = datetime.fromisoformat(snippet['publishedAt'].replace('Z', '+00:00'))
            
            # Get channel details
            channel_response = youtube.channels().list(
                part="snippet",
                id=snippet['channelId']
            ).execute()
            
            channel_data = {}
            if channel_response.get('items'):
                channel_data = channel_response['items'][0]['snippet']
            
            # Construct metadata dictionary
            metadata = {
                "title": snippet.get('title'),
                "channel": snippet.get('channelTitle'),
                "channel_id": snippet.get('channelId'),
                "duration": duration_str,
                "description": snippet.get('description'),
                "views": int(statistics.get('viewCount', 0)),
                "publish_date": publish_date.isoformat() if publish_date else None,
                "keywords": snippet.get('tags', []),
                "thumbnail_url": snippet.get('thumbnails', {}).get('high', {}).get('url'),
                "video_id": video_id,
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "captions": bool(content_details.get('caption') == 'true'),
                "age_restricted": bool(content_details.get('contentRating', {})),
                "rating": round(float(statistics.get('likeCount', 0)) / max(1, float(statistics.get('viewCount', 1))) * 5, 2),
                "length_seconds": duration_seconds,
                "like_count": int(statistics.get('likeCount', 0)),
                "comment_count": int(statistics.get('commentCount', 0)),
                "privacy_status": status.get('privacyStatus'),
                "channel_logo": channel_data.get('thumbnails', {}).get('default', {}).get('url'),
                "metadata_fetched_at": time.time()
            }
            
            logger.info(f"Successfully fetched metadata for video {video_id}")
            return metadata
            
        except Exception as e:
            if attempt == max_retries - 1:
                logger.error(f"Failed to fetch metadata for video {video_id} after {max_retries} attempts: {str(e)}")
                raise Exception(f"Error fetching video metadata: {str(e)}")
            
            logger.warning(f"Attempt {attempt + 1} failed for video {video_id}, retrying...")
            time.sleep(1)  # Wait before retrying

def get_video_transcript(url: str, api_key: str = None) -> str:
    """
    Get video transcript from YouTube using the YouTube Data API.
    
    Note: The YouTube Data API doesn't directly provide transcripts. 
    For transcripts, you would need to use the YouTube Transcript API or similar.
    This is a placeholder that returns caption tracks information.
    """
    api_key = api_key or os.environ.get('YOUTUBE_API_KEY')
    if not api_key:
        raise ValueError("YouTube API key is required. Set it as an argument or YOUTUBE_API_KEY environment variable.")
    
    try:
        video_id = extract_video_id(url)
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        # Get caption tracks
        captions_response = youtube.captions().list(
            part="snippet",
            videoId=video_id
        ).execute()
        
        caption_tracks = []
        if captions_response.get('items'):
            for item in captions_response['items']:
                caption_tracks.append({
                    'id': item['id'],
                    'language': item['snippet'].get('language'),
                    'name': item['snippet'].get('name')
                })
        
        return f"Found {len(caption_tracks)} caption tracks: {caption_tracks}"
        
    except Exception as e:
        raise Exception(f"Error fetching video caption information: {str(e)}")

# Example usage
if __name__ == "__main__":
    # Set API key in environment or pass directly
    # os.environ['YOUTUBE_API_KEY'] = "YOUR_API_KEY_HERE"
    
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    try:
        api_key = "YOUR_API_KEY_HERE"  # Replace with your actual API key
        metadata = get_video_metadata(video_url, api_key=api_key)
        print(f"Video Title: {metadata['title']}")
        print(f"Channel: {metadata['channel']}")
        print(f"Views: {metadata['views']}")
        print(f"Duration: {metadata['duration']} ({metadata['length_seconds']} seconds)")
        
        # Get caption information
        # caption_info = get_video_transcript(video_url, api_key=api_key)
        # print(caption_info)
    except Exception as e:
        print(f"Error: {e}")