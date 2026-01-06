"""Module to fetch papers from arXiv based on keywords."""
import arxiv
from datetime import datetime, timedelta
from typing import List, Dict

class ArxivFetcher:
    """Fetches papers from arXiv based on search keywords."""

    def __init__(self, max_results: int = 5):
        """
        Initialize the arXiv fetcher.

        Args:
            max_results: Maximum number of papers to fetch per keyword
        """
        self.max_results = max_results

    def fetch_recent_papers(self, keywords: List[str] = None, keyword_categories: Dict[str, List[str]] = None, days_back: int = 1) -> List[Dict]:
        """
        Fetch recent papers from arXiv for given keywords.

        Args:
            keywords: List of search keywords (for backward compatibility)
            keyword_categories: Dict of {category: [keywords]} for categorized search
            days_back: Number of days to look back for papers

        Returns:
            List of paper dictionaries with metadata
        """
        all_papers = []
        cutoff_date = datetime.now() - timedelta(days=days_back)
        paper_category_map = {}  # Track assigned categories to avoid duplicates

        # Use categorized keywords if provided, otherwise fall back to simple list
        if keyword_categories:
            # Flatten categories into (keyword, category) pairs
            keyword_list = []
            for category, kw_list in keyword_categories.items():
                for kw in kw_list:
                    keyword_list.append((kw, category))
        else:
            # Backward compatibility: simple keyword list
            keyword_list = [(kw, "General") for kw in (keywords or [])]

        for keyword, category in keyword_list:
            try:
                print(f"Searching arXiv for '{keyword}' (Category: {category})")

                # Create search query
                search = arxiv.Search(
                    query=keyword,
                    max_results=self.max_results * 2,  # Fetch more to filter by date
                    sort_by=arxiv.SortCriterion.SubmittedDate,
                    sort_order=arxiv.SortOrder.Descending
                )

                # Fetch and filter papers
                for paper in search.results():
                    # Check if paper is recent enough
                    if paper.published.replace(tzinfo=None) < cutoff_date:
                        continue

                    paper_id = paper.entry_id

                    # Check if we already have this paper
                    if paper_id in paper_category_map:
                        # Paper already found - skip to avoid duplicates
                        # The first category match is kept
                        continue

                    paper_data = {
                        'id': paper_id,
                        'title': paper.title,
                        'authors': [author.name for author in paper.authors],
                        'summary': paper.summary,
                        'published': paper.published.strftime('%Y-%m-%d'),
                        'pdf_url': paper.pdf_url,
                        'categories': paper.categories,
                        'primary_category': paper.primary_category,
                        'keyword': keyword,
                        'paper_category': category  # Add category classification
                    }

                    all_papers.append(paper_data)
                    paper_category_map[paper_id] = category

                    # Check count per keyword (not per category)
                    if len([p for p in all_papers if p['keyword'] == keyword]) >= self.max_results:
                        break

            except Exception as e:
                print(f"Error fetching papers for keyword '{keyword}': {e}")
                continue

        print(f"Found {len(all_papers)} papers total")
        return all_papers

    def format_paper_info(self, paper: Dict) -> str:
        """
        Format paper information as a readable string.

        Args:
            paper: Paper dictionary

        Returns:
            Formatted string with paper details
        """
        authors_str = ", ".join(paper['authors'][:3])
        if len(paper['authors']) > 3:
            authors_str += f" et al. ({len(paper['authors'])} authors total)"

        return f"""
Title: {paper['title']}
Authors: {authors_str}
Published: {paper['published']}
Category: {paper['primary_category']}
URL: {paper['pdf_url']}

Abstract:
{paper['summary']}
"""
