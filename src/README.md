# YouTube Political Study Scraper

This directory contains the refactored Python script for scraping YouTube channels and collecting video data including comments.

## Features

- Scrapes multiple YouTube channels by handle or ID
- Collects video metadata (title, description, views, likes, etc.)
- Downloads video transcripts
- Collects up to 1000 top comments per video using YoutubeCommentDownloader
- Caches data to avoid re-scraping
- Exports data in JSON and CSV formats
- Respectful rate limiting to avoid API issues

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set your YouTube Data API v3 key as an environment variable:
```bash
export H_YOUTUBE_API_KEY="your_api_key_here"
```

## Usage

### Basic Usage

Run the script with the default YouTubers list:
```bash
python youtube_scraper.py
```

### Custom YouTubers

To modify the list of YouTubers, edit the `youtubers` list in the `main()` function:

```python
youtubers = ['@HasanAbi', '@joerogan', '@your_channel_here']
```

### Configuration Options

You can modify these parameters in the `main()` function:

- `max_videos_per_channel`: Maximum number of videos to process per channel (default: 100)
- `max_comments_per_video`: Maximum comments to collect per video (default: 1000)
- `output_format`: Data export format ('json', 'csv', or 'both')

## Output

The script creates the following files in the `data/` directory:

- `youtube_data_YYYYMMDD_HHMMSS.json`: Complete video data in JSON format
- `youtube_data_YYYYMMDD_HHMMSS.csv`: Video metadata in CSV format
- `youtube_comments_YYYYMMDD_HHMMSS.csv`: All comments in CSV format

## Data Structure

### Video Data
Each video entry contains:
- Channel information (handle, ID)
- Video metadata (ID, title, description, published date, duration)
- Statistics (view count, like count, comment count)
- Transcript text
- List of comments
- Processing timestamp

### Comment Data
Each comment contains:
- Video ID reference
- Comment ID, text, timestamp
- Author information
- Vote count and reply count

## Caching

The script automatically caches data for each channel in the `cache/` directory. If you run the script again, it will skip channels that have already been processed unless you delete the cache files.

## Rate Limiting

The script includes built-in delays to respect YouTube's API limits:
- 1 second between video processing
- 0.1 seconds between comment collection

## Logging

All operations are logged to both console and `youtube_scraper.log` file.

## Error Handling

The script includes comprehensive error handling for:
- API failures
- Missing transcripts
- Network issues
- Invalid channel handles/IDs

## Notes

- YouTube Data API v3 has daily quotas. Monitor your usage.
- Some videos may not have transcripts available.
- Comment collection may be limited by YouTube's policies.
- The script respects YouTube's terms of service and rate limits. 