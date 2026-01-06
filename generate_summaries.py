#!/usr/bin/env python3
"""Script to generate paper summaries for a specific date and save as markdown files."""
import sys
import os
import argparse
from datetime import datetime, timedelta
from arxiv_fetcher import ArxivFetcher
from summarizer import PaperSummarizer
from paper_database import PaperDatabase
from similarity import PaperSimilarity
from figure_extractor import FigureExtractor
from config import Config

def generate_summaries_for_date(target_date: str, output_dir: str = "paper_summaries"):
    """
    Generate paper summaries for a specific date and save as markdown.

    Args:
        target_date: Date in YYYY-MM-DD format
        output_dir: Directory to save markdown files
    """
    try:
        # Validate configuration
        Config.validate()

        # Parse date
        date_obj = datetime.strptime(target_date, '%Y-%m-%d')

        print(f"\n{'='*70}")
        print(f"arXiv Paper Summary Generator - {target_date}")
        print(f"{'='*70}\n")

        # Create output directory
        date_folder = os.path.join(output_dir, target_date)
        os.makedirs(date_folder, exist_ok=True)
        print(f"Output directory: {date_folder}\n")

        # Initialize components
        print("Initializing components...")
        arxiv_fetcher = ArxivFetcher(max_results=Config.MAX_PAPERS_PER_KEYWORD)
        summarizer = PaperSummarizer(api_key=Config.ANTHROPIC_API_KEY)
        paper_db = PaperDatabase()
        similarity_calc = PaperSimilarity()
        figure_extractor = FigureExtractor()

        # Fetch papers for the specific date
        print(f"\nSearching for papers published on {target_date}:")
        print(f"Categories: {list(Config.KEYWORD_CATEGORIES.keys())}\n")

        papers = arxiv_fetcher.fetch_recent_papers(
            keyword_categories=Config.KEYWORD_CATEGORIES,
            days_back=30  # Look back 30 days to catch papers from target date
        )

        # Filter papers for the specific date
        papers_on_date = [p for p in papers if p['published'] == target_date]

        if not papers_on_date:
            print(f"No papers found for {target_date}")
            print(f"Note: Found {len(papers)} papers in the last 30 days")
            # Show available dates
            dates = sorted(set(p['published'] for p in papers))
            if dates:
                print(f"\nAvailable dates in recent papers:")
                for d in dates[-10:]:  # Show last 10 dates
                    count = len([p for p in papers if p['published'] == d])
                    print(f"  - {d}: {count} papers")
            return

        print(f"Found {len(papers_on_date)} papers for {target_date}\n")

        # Get existing papers for similarity
        print("Loading existing papers for similarity matching...")
        existing_papers = paper_db.get_all_papers()
        print(f"Found {len(existing_papers)} papers in database\n")

        # Process each paper
        successful = 0
        failed = 0

        for i, paper in enumerate(papers_on_date, 1):
            print(f"[{i}/{len(papers_on_date)}] Processing: {paper['title'][:60]}...")

            try:
                # Compute embedding
                print("  Computing embedding...")
                embedding = similarity_calc.compute_embedding(paper)
                paper['embedding'] = embedding

                # Extract figures
                figure_paths = []
                try:
                    print("  Extracting figures...")
                    figure_paths = figure_extractor.get_paper_figures(paper, max_figures=2)
                except Exception as e:
                    print(f"    Could not extract figures: {e}")

                # Find similar papers
                similar_papers = []
                if existing_papers:
                    print("  Finding similar papers...")
                    similar_papers = similarity_calc.find_similar_papers(
                        paper,
                        existing_papers,
                        top_k=5
                    )
                    if similar_papers:
                        print(f"    Found {len(similar_papers)} similar papers")

                # Generate summary
                print("  Generating AI summary...")
                summary = summarizer.summarize_paper(paper)

                # Create markdown
                print("  Creating markdown...")
                markdown = summarizer.create_markdown_summary(
                    paper,
                    summary,
                    similar_papers=similar_papers,
                    figure_paths=figure_paths
                )

                # Save to file
                safe_title = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_'
                                    for c in paper['title'])[:100]
                filename = f"{i}_{safe_title}.md"
                filepath = os.path.join(date_folder, filename)

                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(markdown)

                print(f"  ✓ Saved to: {filename}\n")
                successful += 1

            except Exception as e:
                print(f"  ✗ Error: {e}\n")
                failed += 1

        # Summary
        print(f"\n{'='*70}")
        print(f"Summary Generation Complete")
        print(f"{'='*70}")
        print(f"Papers processed: {successful}")
        print(f"Papers failed: {failed}")
        print(f"Output directory: {date_folder}")
        print(f"{'='*70}\n")

        # Create index file
        index_path = os.path.join(date_folder, "INDEX.md")
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(f"# arXiv Papers - {target_date}\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"Total papers: {successful}\n\n")
            f.write("## Papers by Category\n\n")

            for category in Config.KEYWORD_CATEGORIES.keys():
                category_papers = [p for p in papers_on_date if p.get('paper_category') == category]
                if category_papers:
                    f.write(f"### {category} ({len(category_papers)} papers)\n\n")
                    for i, paper in enumerate(category_papers, 1):
                        safe_title = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_'
                                            for c in paper['title'])[:100]
                        # Find the actual filename
                        for j, p in enumerate(papers_on_date, 1):
                            if p['id'] == paper['id']:
                                filename = f"{j}_{safe_title}.md"
                                break
                        f.write(f"{i}. [{paper['title']}](./{filename})\n")
                        f.write(f"   - Authors: {', '.join(paper['authors'][:3])}\n")
                        f.write(f"   - [PDF]({paper['pdf_url']})\n\n")

        print(f"Index file created: INDEX.md\n")
        paper_db.close()

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(
        description="Generate paper summaries for a specific date",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate summaries for a specific date
  python generate_summaries.py --date 2024-01-15

  # Use custom output directory
  python generate_summaries.py --date 2024-01-15 --output my_summaries

  # Generate for yesterday
  python generate_summaries.py --yesterday

  # Generate for today
  python generate_summaries.py --today
        """
    )

    parser.add_argument('--date', type=str, help='Target date (YYYY-MM-DD)')
    parser.add_argument('--today', action='store_true', help='Use today\'s date')
    parser.add_argument('--yesterday', action='store_true', help='Use yesterday\'s date')
    parser.add_argument('--output', type=str, default='paper_summaries',
                       help='Output directory (default: paper_summaries)')

    args = parser.parse_args()

    # Determine target date
    if args.today:
        target_date = datetime.now().strftime('%Y-%m-%d')
    elif args.yesterday:
        target_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    elif args.date:
        target_date = args.date
    else:
        parser.print_help()
        sys.exit(1)

    generate_summaries_for_date(target_date, args.output)

if __name__ == "__main__":
    main()
