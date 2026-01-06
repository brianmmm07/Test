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

    # Search settings - supports categorized keywords
    # Format: "Category1: keyword1, keyword2 | Category2: keyword3, keyword4"
    # Or simple: "keyword1, keyword2, keyword3"
    _KEYWORDS_RAW = os.getenv('KEYWORDS', 'image generation,video generation')

    @classmethod
    def _parse_keywords(cls):
        """
        Parse keywords from config into categories.

        Supports two formats:
        1. Categorized: "Image Generation: keyword1, keyword2 | Video Generation: keyword3"
        2. Simple: "keyword1, keyword2, keyword3" (creates single "General" category)

        Returns:
            dict: {category: [keywords]}
        """
        keywords_raw = cls._KEYWORDS_RAW.strip()

        # Check if format contains categories (has ":" before "|" or in single entry)
        if ':' in keywords_raw:
            # Categorized format
            categories = {}
            category_groups = keywords_raw.split('|')

            for group in category_groups:
                group = group.strip()
                if ':' not in group:
                    continue

                category_name, keywords_str = group.split(':', 1)
                category_name = category_name.strip()
                keywords = [k.strip() for k in keywords_str.split(',') if k.strip()]

                if category_name and keywords:
                    categories[category_name] = keywords

            return categories if categories else {"General": ["image generation", "video generation"]}
        else:
            # Simple format - create General category
            keywords = [k.strip() for k in keywords_raw.split(',') if k.strip()]
            return {"General": keywords if keywords else ["image generation", "video generation"]}

    KEYWORD_CATEGORIES = _parse_keywords.__func__(None)

    # Flat list of all keywords for backward compatibility
    KEYWORDS = [kw for keywords in KEYWORD_CATEGORIES.values() for kw in keywords]

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

    @classmethod
    def get_category_for_keyword(cls, keyword):
        """
        Get the category name for a given keyword.

        Args:
            keyword: The keyword to look up

        Returns:
            str: Category name
        """
        for category, keywords in cls.KEYWORD_CATEGORIES.items():
            if keyword in keywords:
                return category
        return "General"
