#!/usr/bin/env python3
"""
Example usage of the YouTube Political Study Scraper

This script demonstrates how to use the scraper with custom settings.
"""

import os
from dotenv import load_dotenv
from youtube_scraper import YouTubeScraper

# Load environment variables
load_dotenv()

def example_custom_scraping():
    """Example of custom scraping with different settings."""
    
    # Check for API key
    API_KEY = os.getenv("H_YOUTUBE_API_KEY")
    if not API_KEY:
        print("Please set H_YOUTUBE_API_KEY environment variable")
        return
    
    # Initialize scraper
    scraper = YouTubeScraper(API_KEY)
    
    # Custom list of YouTubers
    custom_youtubers = [
        '@HasanAbi',
        '@joerogan',
        '@lexfridman',  # Add more channels as needed
        '@timcast'
    ]
    
    print(f"Starting custom scraping for {len(custom_youtubers)} channels...")
    
    # Fetch videos with custom settings
    videos_data = scraper.fetch_and_process_channel_videos(
        channel_handles=custom_youtubers,
        max_videos_per_channel=50,  # Limit to 50 videos per channel
        max_comments_per_video=500   # Limit to 500 comments per video
    )
    
    # Save data in JSON format only
    scraper.save_data(videos_data, output_format='json')
    
    print(f"Custom scraping completed! Processed {len(videos_data)} videos")

def example_single_channel():
    """Example of scraping a single channel."""
    
    API_KEY = os.getenv("H_YOUTUBE_API_KEY")
    if not API_KEY:
        print("Please set H_YOUTUBE_API_KEY environment variable")
        return
    
    scraper = YouTubeScraper(API_KEY)
    
    # Single channel
    single_channel = ['@HasanAbi']
    
    print(f"Starting single channel scraping for {single_channel[0]}...")
    
    videos_data = scraper.fetch_and_process_channel_videos(
        channel_handles=single_channel,
        max_videos_per_channel=10,  # Just 10 videos for testing
        max_comments_per_video=100   # Just 100 comments for testing
    )
    
    # Save in both formats
    scraper.save_data(videos_data, output_format='both')
    
    print(f"Single channel scraping completed! Processed {len(videos_data)} videos")

if __name__ == "__main__":
    print("YouTube Political Study Scraper - Example Usage")
    print("=" * 50)
    
    # Run examples
    print("\n1. Custom scraping example:")
    example_custom_scraping()
    
    print("\n2. Single channel example:")
    example_single_channel()
    
    print("\nExamples completed!") 