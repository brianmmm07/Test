"""Configuration management for arXiv summarizer."""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration."""

    # API Keys
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    NOTION_TOKEN = os.getenv('NOTION_TOKEN')
    NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID')

    # Search settings
    KEYWORDS = os.getenv('KEYWORDS', 'image generation,video generation').split(',')
    KEYWORDS = [k.strip() for k in KEYWORDS]

    MAX_PAPERS_PER_KEYWORD = int(os.getenv('MAX_PAPERS_PER_KEYWORD', '5'))

    # Schedule settings
    SCHEDULE_TIME = os.getenv('SCHEDULE_TIME', '09:00')

    @classmethod
    def validate(cls):
        """Validate required configuration."""
        missing = []
        if not cls.ANTHROPIC_API_KEY:
            missing.append('ANTHROPIC_API_KEY')
        if not cls.NOTION_TOKEN:
            missing.append('NOTION_TOKEN')
        if not cls.NOTION_DATABASE_ID:
            missing.append('NOTION_DATABASE_ID')

        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

        return True
