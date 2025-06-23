# YouTube Political Study Scraper

A comprehensive Python tool for scraping YouTube channels and collecting video data including comments for political research and analysis.

## Overview

This project refactors the original Jupyter notebook into a modular Python script that can:

- Scrape multiple YouTube channels by handle or ID
- Collect comprehensive video metadata (title, description, views, likes, etc.)
- Download video transcripts
- Collect up to 1000 top comments per video using YoutubeCommentDownloader
- Cache data to avoid re-scraping
- Export data in JSON and CSV formats
- Respect YouTube's API limits and terms of service

## Quick Start

### 1. Setup

```bash
cd src
python setup.py
```

### 2. Get YouTube API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable YouTube Data API v3
4. Create credentials (API Key)
5. Set the environment variable:
```bash
export H_YOUTUBE_API_KEY="your_api_key_here"
```

### 3. Run the Scraper

```bash
python youtube_scraper.py
```

This will scrape the default channels: `@HasanAbi` and `@joerogan`

## Configuration

Edit `src/config.py` to customize:

- **YOUTUBERS**: List of channel handles to scrape
- **MAX_VIDEOS_PER_CHANNEL**: Maximum videos per channel (default: 100)
- **MAX_COMMENTS_PER_VIDEO**: Maximum comments per video (default: 1000)
- **OUTPUT_FORMAT**: Export format ('json', 'csv', or 'both')
- **Rate limiting**: Delays between requests

## Output

The scraper creates:

- `data/youtube_data_YYYYMMDD_HHMMSS.json`: Complete video data
- `data/youtube_data_YYYYMMDD_HHMMSS.csv`: Video metadata
- `data/youtube_comments_YYYYMMDD_HHMMSS.csv`: All comments
- `cache/`: Cached data to avoid re-scraping

## Data Structure

### Video Data
```json
{
  "channel_handle": "@HasanAbi",
  "channel_id": "UC3mvN-7gQ5RpOrjk2IlGTFA",
  "video_id": "abc123",
  "title": "Video Title",
  "description": "Video description...",
  "published_at": "2024-01-01T00:00:00Z",
  "duration": "PT1H30M",
  "view_count": "1000000",
  "like_count": "50000",
  "comment_count": "1000",
  "transcript": "Full video transcript...",
  "comments": [...],
  "processed_at": "2024-01-01T12:00:00"
}
```

### Comment Data
```json
{
  "cid": "comment_id",
  "text": "Comment text",
  "time": "2 hours ago",
  "author": "@username",
  "channel": "channel_id",
  "votes": "100",
  "replies": "5"
}
```

## Examples

### Custom Scraping
```python
from youtube_scraper import YouTubeScraper

scraper = YouTubeScraper(API_KEY)
videos_data = scraper.fetch_and_process_channel_videos(
    channel_handles=['@HasanAbi', '@joerogan'],
    max_videos_per_channel=50,
    max_comments_per_video=500
)
scraper.save_data(videos_data, output_format='both')
```

### Single Channel
```python
# See example_usage.py for more examples
python example_usage.py
```

## Features

- **Caching**: Automatically caches channel data to avoid re-scraping
- **Rate Limiting**: Built-in delays to respect API limits
- **Error Handling**: Comprehensive error handling and logging
- **Flexible Output**: JSON and CSV export options
- **Transcript Support**: Downloads video transcripts when available
- **Comment Collection**: Uses YoutubeCommentDownloader for reliable comment scraping

## Requirements

- Python 3.7+
- YouTube Data API v3 key
- Internet connection

## Dependencies

- `google-api-python-client`: YouTube API client
- `youtube-transcript-api`: Video transcript download
- `yt-dlp`: YouTube data extraction
- `youtube-comment-downloader`: Comment collection
- `pandas`: Data manipulation and export

## Rate Limits

- YouTube Data API v3: 10,000 units per day (free tier)
- Built-in delays: 1 second between videos, 0.1 seconds between comments
- Respects YouTube's terms of service

## Notes

- Monitor your API quota usage
- Some videos may not have transcripts
- Comment collection may be limited by YouTube policies
- The script is designed for research purposes and respects platform terms

## License

MIT License - see LICENSE file for details.

## Contributing

Feel free to submit issues and enhancement requests!