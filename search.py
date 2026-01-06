#!/usr/bin/env python3
"""Search tool for querying the paper database."""
import argparse
import sys
from paper_database import PaperDatabase
from similarity import PaperSimilarity
from datetime import datetime, timedelta

def display_paper(paper: dict, show_details: bool = False):
    """Display a paper in a formatted way."""
    print(f"\n{'='*70}")
    print(f"Title: {paper['title']}")
    print(f"Authors: {', '.join(paper['authors'][:3])}{' et al.' if len(paper['authors']) > 3 else ''}")
    print(f"Published: {paper['published']}")
    print(f"Category: {paper['paper_category']}")
    print(f"PDF: {paper['pdf_url']}")

    if show_details:
        print(f"\nAbstract:")
        print(f"{paper['summary'][:300]}..." if len(paper['summary']) > 300 else paper['summary'])

def search_by_author(db: PaperDatabase, author_name: str):
    """Search papers by author name."""
    print(f"\nSearching for papers by author: {author_name}")
    papers = db.search_by_author(author_name)

    if not papers:
        print("No papers found.")
        return

    print(f"\nFound {len(papers)} paper(s):")
    for paper in papers:
        display_paper(paper)

def search_by_date_range(db: PaperDatabase, start_date: str, end_date: str):
    """Search papers by date range."""
    print(f"\nSearching for papers from {start_date} to {end_date}")
    papers = db.search_by_date_range(start_date, end_date)

    if not papers:
        print("No papers found.")
        return

    print(f"\nFound {len(papers)} paper(s):")
    for paper in papers:
        display_paper(paper)

def search_by_category(db: PaperDatabase, category: str):
    """Search papers by category."""
    print(f"\nSearching for papers in category: {category}")
    papers = db.get_papers_by_category(category)

    if not papers:
        print("No papers found.")
        return

    print(f"\nFound {len(papers)} paper(s):")
    for paper in papers:
        display_paper(paper)

def find_similar(db: PaperDatabase, paper_id: str):
    """Find similar papers to a given paper."""
    paper = db.get_paper(paper_id)
    if not paper:
        print(f"Paper not found: {paper_id}")
        return

    print(f"\nFinding papers similar to:")
    display_paper(paper, show_details=True)

    similar_papers = db.get_similar_papers(paper_id, top_k=10)

    if not similar_papers:
        print("\nNo similar papers found in database.")
        return

    print(f"\nTop {len(similar_papers)} most similar papers:")
    for i, (similar_paper, score) in enumerate(similar_papers, 1):
        print(f"\n{i}. Similarity: {int(score * 100)}%")
        display_paper(similar_paper)

def list_recent(db: PaperDatabase, limit: int = 10):
    """List recent papers."""
    print(f"\nListing {limit} most recent papers:")
    papers = db.get_all_papers(limit=limit)

    if not papers:
        print("No papers found.")
        return

    for paper in papers:
        display_paper(paper)

def show_statistics(db: PaperDatabase):
    """Show database statistics."""
    stats = db.get_statistics()

    print("\n" + "="*70)
    print("DATABASE STATISTICS")
    print("="*70)
    print(f"\nTotal Papers: {stats['total_papers']}")

    print(f"\nPapers by Category:")
    for category, count in sorted(stats['papers_by_category'].items(), key=lambda x: x[1], reverse=True):
        print(f"  - {category}: {count}")

    print(f"\nDate Range:")
    print(f"  - Earliest: {stats['date_range']['earliest']}")
    print(f"  - Latest: {stats['date_range']['latest']}")

    print(f"\nSimilarity Connections: {stats['total_similarities']}")
    print("="*70 + "\n")

def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description="Search and query the arXiv paper database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search by author
  python search.py --author "Andrew Ng"

  # Search by date range
  python search.py --date-range 2024-01-01 2024-12-31

  # Search by category
  python search.py --category "Image Generation"

  # Find similar papers
  python search.py --similar "http://arxiv.org/abs/2401.12345"

  # List recent papers
  python search.py --recent 20

  # Show statistics
  python search.py --stats
        """
    )

    parser.add_argument('--author', type=str, help='Search by author name')
    parser.add_argument('--date-range', nargs=2, metavar=('START', 'END'),
                       help='Search by date range (YYYY-MM-DD)')
    parser.add_argument('--category', type=str, help='Search by category')
    parser.add_argument('--similar', type=str, help='Find similar papers (arXiv ID or URL)')
    parser.add_argument('--recent', type=int, metavar='N', help='List N most recent papers')
    parser.add_argument('--stats', action='store_true', help='Show database statistics')
    parser.add_argument('--db-path', type=str, default='papers.db',
                       help='Path to database file (default: papers.db)')

    args = parser.parse_args()

    # Initialize database
    db = PaperDatabase(db_path=args.db_path)

    try:
        if args.author:
            search_by_author(db, args.author)

        elif args.date_range:
            start_date, end_date = args.date_range
            search_by_date_range(db, start_date, end_date)

        elif args.category:
            search_by_category(db, args.category)

        elif args.similar:
            # Extract arxiv ID from URL if needed
            paper_id = args.similar
            if 'arxiv.org' in paper_id:
                paper_id = paper_id.split('/')[-1]
            if not paper_id.startswith('http'):
                paper_id = f"http://arxiv.org/abs/{paper_id}"
            find_similar(db, paper_id)

        elif args.recent:
            list_recent(db, args.recent)

        elif args.stats:
            show_statistics(db)

        else:
            parser.print_help()

    finally:
        db.close()

if __name__ == "__main__":
    main()
