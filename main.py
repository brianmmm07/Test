"""Main application for arXiv paper summarizer."""
import sys
from datetime import datetime
from arxiv_fetcher import ArxivFetcher
from summarizer import PaperSummarizer
from notion_client import NotionClient
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

        # Verify Notion connection
        print("Verifying Notion connection...")
        notion_client.create_database_if_needed()

        # Fetch papers
        print(f"\nSearching for papers with keywords: {', '.join(Config.KEYWORDS)}")
        papers = arxiv_fetcher.fetch_recent_papers(Config.KEYWORDS)

        if not papers:
            print("No new papers found.")
            return

        print(f"\nProcessing {len(papers)} papers...\n")

        # Process each paper
        successful = 0
        failed = 0

        for i, paper in enumerate(papers, 1):
            print(f"[{i}/{len(papers)}] Processing: {paper['title'][:60]}...")

            try:
                # Generate summary
                summary = summarizer.summarize_paper(paper)

                # Create markdown document
                markdown = summarizer.create_markdown_summary(paper, summary)

                # Add to Notion
                success = notion_client.add_paper(paper, markdown)

                if success:
                    successful += 1
                else:
                    failed += 1

            except Exception as e:
                print(f"Error processing paper: {e}")
                failed += 1

        # Summary
        print(f"\n{'='*60}")
        print(f"Summary: {successful} papers added, {failed} failed")
        print(f"{'='*60}\n")

    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Please check your .env file and ensure all required variables are set.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_daily_summary()
