#!/usr/bin/env python3
"""
YouTube Political Study Scraper

This script refactors the notebook functionality to scrape YouTube channels
and collect video data including comments using YoutubeCommentDownloader.
"""

import os
import json
import logging
import time
import pickle
from typing import List, Dict, Optional, Any
from datetime import datetime
from pathlib import Path
import dotenv
from itertools import islice

import pandas as pd
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from yt_dlp import YoutubeDL
from youtube_comment_downloader import *

# Load environment variables
dotenv.load_dotenv()

# Import configuration
from config import *

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class YouTubeScraper:
    """Main class for YouTube scraping functionality."""
    
    def __init__(self, api_key: str):
        """
        Initialize the YouTube scraper.
        
        Args:
            api_key: YouTube Data API v3 key
        """
        self.api_key = api_key
        self.youtube = build("youtube", "v3", developerKey=api_key)
        self.comment_downloader = YoutubeCommentDownloader()
        
        # Create output directories
        self.output_dir = Path(OUTPUT_DIR)
        self.output_dir.mkdir(exist_ok=True)
        
        self.cache_dir = Path(CACHE_DIR)
        self.cache_dir.mkdir(exist_ok=True)
    
    def get_channel_stats(self, channel_id: str) -> Optional[Dict]:
        """
        Get channel statistics.
        
        Args:
            channel_id: YouTube channel ID
            
        Returns:
            Dictionary with channel statistics or None if failed
        """
        try:
            response = self.youtube.channels().list(
                part="statistics,snippet",
                id=channel_id
            ).execute()
            
            if response['items']:
                return response['items'][0]
            return None
        except Exception as e:
            logger.error(f"Error getting channel stats for {channel_id}: {e}")
            return None
    
    def get_channel_upload_playlist(self, channel_handle: str, channel_id: str = None, by_handle: bool = True) -> Optional[str]:
        """
        Get channel upload playlist ID.
        
        Args:
            channel_handle: YouTube channel handle
            channel_id: YouTube channel ID (optional)
            by_handle: Whether to search by handle or ID
            
        Returns:
            Upload playlist ID or None if failed
        """
        try:
            if by_handle:
                response = self.youtube.channels().list(
                    part="contentDetails",
                    forHandle=channel_handle
                ).execute()
            else:
                response = self.youtube.channels().list(
                    part="contentDetails",
                    id=channel_id
                ).execute()
            
            if response['items']:
                return response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            return None
        except Exception as e:
            logger.error(f"Error getting upload playlist for {channel_handle}: {e}")
            return None
    
    def get_playlist_videos(self, playlist_id: str, max_results: int = 50) -> List[Dict]:
        """
        Get videos from a playlist.
        
        Args:
            playlist_id: YouTube playlist ID
            max_results: Maximum number of videos to retrieve
            
        Returns:
            List of video dictionaries
        """
        videos = []
        next_page_token = None
        
        try:
            while len(videos) < max_results:
                request = self.youtube.playlistItems().list(
                    part="snippet,contentDetails",
                    playlistId=playlist_id,
                    maxResults=min(50, max_results - len(videos)),
                    pageToken=next_page_token
                )
                response = request.execute()
                
                videos.extend(response['items'])
                next_page_token = response.get('nextPageToken')
                
                if not next_page_token:
                    break
                    
        except Exception as e:
            logger.error(f"Error getting playlist videos for {playlist_id}: {e}")
        
        return videos
    
    def get_video_details(self, video_id: str) -> Optional[Dict]:
        """
        Get detailed video information.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Video details dictionary or None if failed
        """
        try:
            response = self.youtube.videos().list(
                part="snippet,statistics,contentDetails",
                id=video_id
            ).execute()
            
            if response['items']:
                return response['items'][0]
            return None
        except Exception as e:
            logger.error(f"Error getting video details for {video_id}: {e}")
            return None
    
    def get_video_transcript(self, video_id: str) -> Optional[str]:
        """
        Get video transcript.
        
        Args:
            video_id: YouTube video ID
            
        Returns:
            Transcript text or None if failed
        """
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            transcript_text = " ".join([item['text'] for item in transcript_list])
            return transcript_text
        except Exception as e:
            logger.warning(f"Could not get transcript for {video_id}: {e}")
            return None
    
    def get_video_comments(self, video_id: str, max_comments: int = 1000) -> List[Dict]:
        """
        Get video comments using YoutubeCommentDownloader with itertools.islice.
        
        Args:
            video_id: YouTube video ID
            max_comments: Maximum number of comments to retrieve
            
        Returns:
            List of comment dictionaries
        """
        comments = []
        try:
            # Create video URL
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            
            # Get comments using get_comments_from_url with popular sorting
            comment_generator = self.comment_downloader.get_comments_from_url(
                video_url, 
                sort_by=SORT_BY_POPULAR
            )
            
            # Use itertools.islice to limit the number of comments
            for comment in islice(comment_generator, max_comments):
                # Clean and structure comment data
                comment_data = {
                    'cid': comment.get('cid', ''),
                    'text': comment.get('text', ''),
                    'time': comment.get('time', ''),
                    'author': comment.get('author', ''),
                    'channel': comment.get('channel', ''),
                    'votes': comment.get('votes', ''),
                    'replies': comment.get('replies', ''),
                    'photo': comment.get('photo', '')
                }
                comments.append(comment_data)
                
                # Add small delay to be respectful
                time.sleep(DELAY_BETWEEN_COMMENTS)
                
        except Exception as e:
            logger.error(f"Error getting comments for {video_id}: {e}")
        
        return comments
    
    def fetch_and_process_channel_videos(self, channel_handles: List[str], 
                                       channel_ids: List[str] = None, 
                                       by_handle: bool = True,
                                       max_videos_per_channel: int = 100,
                                       max_comments_per_video: int = 1000) -> List[Dict]:
        """
        Fetch and process videos from multiple channels.
        
        Args:
            channel_handles: List of YouTube channel handles
            channel_ids: List of YouTube channel IDs (optional)
            by_handle: Whether to search by handle or ID
            max_videos_per_channel: Maximum videos to process per channel
            max_comments_per_video: Maximum comments to collect per video
            
        Returns:
            List of processed video data dictionaries
        """
        all_videos_data = []
        
        for i, channel_handle in enumerate(channel_handles):
            logger.info(f"Processing channel {i+1}/{len(channel_handles)}: {channel_handle}")
            
            # Define cache file paths for this channel
            cache_file = self.cache_dir / f"{channel_handle.replace('@', '')}_videos.pkl"
            video_list_cache_file = self.cache_dir / f"{channel_handle.replace('@', '')}_videos_list.json"
            
            # Check if we have cached mined data
            if cache_file.exists():
                logger.info(f"Loading cached mined data for {channel_handle}")
                try:
                    with open(cache_file, 'rb') as f:
                        cached_data = pickle.load(f)
                    all_videos_data.extend(cached_data)
                    continue
                except Exception as e:
                    logger.warning(f"Failed to load mined data cache for {channel_handle}: {e}")
            
            # Get channel upload playlist
            channel_id = channel_ids[i] if channel_ids and i < len(channel_ids) else None
            playlist_id = self.get_channel_upload_playlist(channel_handle, channel_id, by_handle)
            
            if not playlist_id:
                logger.error(f"Could not get upload playlist for {channel_handle}")
                continue
            
            # Try to load video list from cache
            videos = None
            if video_list_cache_file.exists():
                logger.info(f"Loading video list from cache for {channel_handle}")
                try:
                    with open(video_list_cache_file, 'r', encoding='utf-8') as f:
                        videos = json.load(f)
                except Exception as e:
                    logger.warning(f"Failed to load video list cache for {channel_handle}: {e}")
            
            # If not cached, fetch from API and cache
            if videos is None:
                logger.info(f"Fetching video list from API for {channel_handle}")
                videos = self.get_playlist_videos(playlist_id, max_videos_per_channel)
                try:
                    with open(video_list_cache_file, 'w', encoding='utf-8') as f:
                        json.dump(videos, f, ensure_ascii=False, indent=2)
                    logger.info(f"Cached video list for {channel_handle}")
                except Exception as e:
                    logger.warning(f"Failed to cache video list for {channel_handle}: {e}")
            else:
                logger.info(f"Found {len(videos)} videos for {channel_handle} (from cache)")
            
            channel_videos_data = []
            
            for j, video in enumerate(videos):
                video_id = video['contentDetails']['videoId'] if 'contentDetails' in video and 'videoId' in video['contentDetails'] else video.get('video_id')
                logger.info(f"Processing video {j+1}/{len(videos)}: {video_id}")
                
                # Get detailed video information
                video_details = self.get_video_details(video_id)
                if not video_details:
                    continue
                
                # Get video transcript
                transcript = self.get_video_transcript(video_id)
                
                # Get video comments
                comments = self.get_video_comments(video_id, max_comments_per_video)
                logger.info(f"Collected {len(comments)} comments for {video_id}")
                
                # Structure video data
                video_data = {
                    'channel_handle': channel_handle,
                    'channel_id': video_details['snippet']['channelId'],
                    'video_id': video_id,
                    'title': video_details['snippet']['title'],
                    'description': video_details['snippet']['description'],
                    'published_at': video_details['snippet']['publishedAt'],
                    'duration': video_details['contentDetails']['duration'],
                    'view_count': video_details['statistics'].get('viewCount', 0),
                    'like_count': video_details['statistics'].get('likeCount', 0),
                    'comment_count': video_details['statistics'].get('commentCount', 0),
                    'transcript': transcript,
                    'comments': comments,
                    'processed_at': datetime.now().isoformat()
                }
                
                channel_videos_data.append(video_data)
                
                # Incremental cache every 50 videos
                if (j + 1) % 50 == 0 or (j + 1) == len(videos):
                    try:
                        with open(cache_file, 'wb') as f:
                            pickle.dump(channel_videos_data, f)
                        logger.info(f"Incrementally cached {len(channel_videos_data)} videos for {channel_handle}")
                    except Exception as e:
                        logger.warning(f"Failed to incrementally cache data for {channel_handle}: {e}")
                
                # Add delay between videos to be respectful
                time.sleep(DELAY_BETWEEN_VIDEOS)
            
            all_videos_data.extend(channel_videos_data)
        
        return all_videos_data
    
    def save_data(self, videos_data: List[Dict], output_format: str = 'json') -> None:
        """
        Save collected data to files.
        
        Args:
            videos_data: List of video data dictionaries
            output_format: Output format ('json', 'csv', or 'both')
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if output_format in ['json', 'both']:
            # Save as JSON
            json_file = self.output_dir / f"youtube_data_{timestamp}.json"
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(videos_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved data to {json_file}")
        
        if output_format in ['csv', 'both']:
            # Save as CSV (flattened structure)
            csv_data = []
            for video in videos_data:
                video_row = {
                    'channel_handle': video['channel_handle'],
                    'channel_id': video['channel_id'],
                    'video_id': video['video_id'],
                    'title': video['title'],
                    'description': video['description'],
                    'published_at': video['published_at'],
                    'duration': video['duration'],
                    'view_count': video['view_count'],
                    'like_count': video['like_count'],
                    'comment_count': video['comment_count'],
                    'transcript': video['transcript'],
                    'comments_count': len(video['comments']),
                    'processed_at': video['processed_at']
                }
                csv_data.append(video_row)
            
            csv_file = self.output_dir / f"youtube_data_{timestamp}.csv"
            df = pd.DataFrame(csv_data)
            df.to_csv(csv_file, index=False, encoding='utf-8')
            logger.info(f"Saved data to {csv_file}")
            
            # Save comments separately
            comments_data = []
            for video in videos_data:
                for comment in video['comments']:
                    comment_row = {
                        'video_id': video['video_id'],
                        'channel_handle': video['channel_handle'],
                        'comment_id': comment['cid'],
                        'comment_text': comment['text'],
                        'comment_time': comment['time'],
                        'comment_author': comment['author'],
                        'comment_channel': comment['channel'],
                        'comment_votes': comment['votes'],
                        'comment_replies': comment['replies']
                    }
                    comments_data.append(comment_row)
            
            comments_csv_file = self.output_dir / f"youtube_comments_{timestamp}.csv"
            comments_df = pd.DataFrame(comments_data)
            comments_df.to_csv(comments_csv_file, index=False, encoding='utf-8')
            logger.info(f"Saved comments to {comments_csv_file}")


def main():
    """Main function to run the YouTube scraper."""
    # Get API key from environment
    API_KEY = os.getenv("H_YOUTUBE_API_KEY")
    if not API_KEY:
        logger.error("Please set H_YOUTUBE_API_KEY environment variable")
        return
    
    # Initialize scraper
    scraper = YouTubeScraper(API_KEY)
    
    # Fetch and process videos using config settings
    logger.info(f"Starting to scrape {len(YOUTUBERS)} channels: {YOUTUBERS}")
    videos_data = scraper.fetch_and_process_channel_videos(
        channel_handles=YOUTUBERS,
        max_videos_per_channel=MAX_VIDEOS_PER_CHANNEL,
        max_comments_per_video=MAX_COMMENTS_PER_VIDEO
    )
    
    # Save data using config setting
    scraper.save_data(videos_data, output_format=OUTPUT_FORMAT)
    
    logger.info(f"Scraping completed! Processed {len(videos_data)} videos")


if __name__ == "__main__":
    main() 