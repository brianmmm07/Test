"""Main application for arXiv paper summarizer."""
import sys
from datetime import datetime
from arxiv_fetcher import ArxivFetcher
from summarizer import PaperSummarizer
from notion_client import NotionClient
from paper_database import PaperDatabase
from similarity import PaperSimilarity
from figure_extractor import FigureExtractor
from config import Config

def run_daily_summary():
    """Run the daily paper summary workflow."""
    try:
        # Validate configuration
        Config.validate()
        print(f"\n{'='*60}")
        print(f"arXiv Paper Summarizer - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")

        # Initialize components
        print("Initializing components...")
        arxiv_fetcher = ArxivFetcher(max_results=Config.MAX_PAPERS_PER_KEYWORD)
        summarizer = PaperSummarizer(api_key=Config.ANTHROPIC_API_KEY)
        notion_client = NotionClient(
            token=Config.NOTION_TOKEN,
            database_id=Config.NOTION_DATABASE_ID
        )
        paper_db = PaperDatabase()
        similarity_calc = PaperSimilarity()
        figure_extractor = FigureExtractor()

        # Verify Notion connection
        print("Verifying Notion connection...")
        notion_client.create_database_if_needed()

        # Fetch papers with categorized keywords
        print(f"\nSearching for papers in {len(Config.KEYWORD_CATEGORIES)} categories:")
        for category, keywords in Config.KEYWORD_CATEGORIES.items():
            print(f"  - {category}: {', '.join(keywords)}")

        papers = arxiv_fetcher.fetch_recent_papers(keyword_categories=Config.KEYWORD_CATEGORIES)

        if not papers:
            print("No new papers found.")
            return

        print(f"\nProcessing {len(papers)} papers...\n")

        # Get existing papers from database for similarity matching
        print("Loading existing papers from database for similarity matching...")
        existing_papers = paper_db.get_all_papers()
        print(f"Found {len(existing_papers)} existing papers in database\n")

        # Process each paper
        successful = 0
        failed = 0

        for i, paper in enumerate(papers, 1):
            print(f"[{i}/{len(papers)}] Processing: {paper['title'][:60]}...")

            try:
                # Compute embedding for similarity
                print("  Computing paper embedding...")
                embedding = similarity_calc.compute_embedding(paper)
                paper['embedding'] = embedding

                # Extract figures from PDF (for visual big picture)
                figure_paths = []
                try:
                    figure_paths = figure_extractor.get_paper_figures(paper, max_figures=2)
                except Exception as e:
                    print(f"    Could not extract figures: {e}")

                # Find similar papers
                if existing_papers:
                    print("  Finding similar papers...")
                    similar_papers = similarity_calc.find_similar_papers(
                        paper,
                        existing_papers,
                        top_k=5
                    )

                    # Display similar papers
                    if similar_papers:
                        print(f"  Found {len(similar_papers)} similar papers:")
                        for similar_paper, score in similar_papers[:3]:
                            print(f"    - {similar_paper['title'][:50]}... (similarity: {score:.3f})")
                else:
                    similar_papers = []

                # Generate summary
                print("  Generating AI summary...")
                summary = summarizer.summarize_paper(paper)

                # Create markdown document with similar papers and figures
                print("  Creating markdown with figures and related papers...")
                markdown = summarizer.create_markdown_summary(
                    paper, summary, similar_papers=similar_papers, figure_paths=figure_paths
                )

                # Add to Notion
                print("  Adding to Notion...")
                notion_page_id = notion_client.add_paper(paper, markdown, similar_papers=similar_papers, figure_paths=figure_paths)

                if notion_page_id:
                    # Add to local database
                    print("  Saving to local database...")
                    paper_db.add_paper(paper, embedding=embedding, notion_page_id=notion_page_id)

                    # Store similarity relationships
                    for similar_paper, score in similar_papers:
                        paper_db.add_similarity(paper['id'], similar_paper['id'], score)

                    successful += 1
                    print("  ✓ Complete\n")
                else:
                    failed += 1
                    print("  ✗ Failed to add to Notion\n")

            except Exception as e:
                print(f"  ✗ Error processing paper: {e}\n")
                failed += 1

        # Display statistics
        print(f"\n{'='*60}")
        print(f"Processing Summary:")
        print(f"  - Papers added: {successful}")
        print(f"  - Papers failed: {failed}")
        print(f"{'='*60}\n")

        # Database statistics
        stats = paper_db.get_statistics()
        print("Database Statistics:")
        print(f"  - Total papers: {stats['total_papers']}")
        print(f"  - Papers by category:")
        for category, count in stats['papers_by_category'].items():
            print(f"    * {category}: {count}")
        print(f"  - Date range: {stats['date_range']['earliest']} to {stats['date_range']['latest']}")
        print(f"  - Similarity connections: {stats['total_similarities']}")
        print(f"{'='*60}\n")

        # Close database
        paper_db.close()

    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Please check your .env file and ensure all required variables are set.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_daily_summary()
