"""
Configuration file for YouTube Political Study Scraper
"""

# List of YouTubers to scrape (channel handles)
YOUTUBERS = [
    '@HasanAbi',
    '@joerogan'
]

# YouTube Data API v3 key (set as environment variable H_YOUTUBE_API_KEY)
# export H_YOUTUBE_API_KEY="your_api_key_here"

# Scraping settings
MAX_VIDEOS_PER_CHANNEL = 4000  # Maximum videos to process per channel
MAX_COMMENTS_PER_VIDEO = 200  # Maximum comments to collect per video

# Output settings
OUTPUT_FORMAT = 'both'  # 'json', 'csv', or 'both'

# Rate limiting (in seconds)
DELAY_BETWEEN_VIDEOS = 0.5  # Delay between processing videos
DELAY_BETWEEN_COMMENTS = 0  # Delay between collecting comments

# File paths
OUTPUT_DIR = "data"  # Directory for output files
CACHE_DIR = "cache"  # Directory for cache files
LOG_FILE = "youtube_scraper.log"  # Log file name

# Comment sorting (for YoutubeCommentDownloader)
# 0 = Sort by relevance, 1 = Sort by recent
COMMENT_SORT_BY = 0 