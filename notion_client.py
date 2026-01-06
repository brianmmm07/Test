"""Module to interact with Notion API."""
from notion_client import Client
from typing import Dict, List
from datetime import datetime

class NotionClient:
    """Client for sending paper summaries to Notion."""

    def __init__(self, token: str, database_id: str):
        """
        Initialize Notion client.

        Args:
            token: Notion integration token
            database_id: ID of the Notion database
        """
        self.client = Client(auth=token)
        self.database_id = database_id

    def create_database_if_needed(self):
        """
        Verify database exists and has correct schema.
        Note: This requires the database to be shared with the integration.
        """
        try:
            self.client.databases.retrieve(database_id=self.database_id)
            print(f"Connected to Notion database: {self.database_id}")
        except Exception as e:
            print(f"Error accessing database: {e}")
            print("Make sure the database is shared with your Notion integration.")
            raise

    def add_paper(self, paper: Dict, markdown_summary: str, similar_papers: list = None, figure_paths: list = None) -> str:
        """
        Add a paper summary to the Notion database.

        Args:
            paper: Paper dictionary
            markdown_summary: Full markdown summary
            similar_papers: List of (paper_dict, similarity_score) tuples
            figure_paths: List of paths to extracted figure images

        Returns:
            Notion page ID if successful, None otherwise
        """
        try:
            # Prepare authors string
            authors_str = ", ".join(paper['authors'][:3])
            if len(paper['authors']) > 3:
                authors_str += f" et al."

            # Create page properties
            # Use paper_category for organization, primary_category for arXiv classification
            paper_category = paper.get('paper_category', 'General')

            properties = {
                "Title": {
                    "title": [
                        {
                            "text": {
                                "content": paper['title']
                            }
                        }
                    ]
                },
                "Authors": {
                    "rich_text": [
                        {
                            "text": {
                                "content": authors_str
                            }
                        }
                    ]
                },
                "Published": {
                    "date": {
                        "start": paper['published']
                    }
                },
                "Category": {
                    "select": {
                        "name": paper_category  # Use our category classification
                    }
                },
                "arXiv Category": {
                    "select": {
                        "name": paper['primary_category']  # Keep arXiv's category
                    }
                },
                "Keywords": {
                    "multi_select": [
                        {"name": paper['keyword']}
                    ]
                },
                "URL": {
                    "url": paper['pdf_url']
                }
            }

            # Convert markdown to Notion blocks
            children = self._markdown_to_blocks(markdown_summary)

            # Create page
            response = self.client.pages.create(
                parent={"database_id": self.database_id},
                properties=properties,
                children=children
            )

            page_id = response['id']
            print(f"Added paper to Notion: {paper['title'][:50]}...")
            return page_id

        except Exception as e:
            print(f"Error adding paper to Notion: {e}")
            return None

    def _markdown_to_blocks(self, markdown: str) -> List[Dict]:
        """
        Convert markdown text to Notion blocks.

        Args:
            markdown: Markdown text

        Returns:
            List of Notion block objects
        """
        blocks = []
        lines = markdown.split('\n')

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            if not line:
                i += 1
                continue

            # Heading 1
            if line.startswith('# '):
                blocks.append({
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {
                        "rich_text": [{"type": "text", "text": {"content": line[2:]}}]
                    }
                })
            # Heading 2
            elif line.startswith('## '):
                blocks.append({
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": line[3:]}}]
                    }
                })
            # Heading 3
            elif line.startswith('### '):
                blocks.append({
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{"type": "text", "text": {"content": line[4:]}}]
                    }
                })
            # Image (markdown syntax: ![alt](path))
            elif line.startswith('![') and '](' in line:
                # Extract alt text and path
                import re
                match = re.match(r'!\[(.*?)\]\((.*?)\)', line)
                if match:
                    alt_text = match.group(1)
                    # Create a callout block noting the figure
                    blocks.append({
                        "object": "block",
                        "type": "callout",
                        "callout": {
                            "rich_text": [{
                                "type": "text",
                                "text": {"content": f"📊 {alt_text} - See figures in the PDF linked above"}
                            }],
                            "icon": {"emoji": "📊"}
                        }
                    })
            # Bullet point
            elif line.startswith('- ') or line.startswith('* '):
                blocks.append({
                    "object": "block",
                    "type": "bulleted_list_item",
                    "bulleted_list_item": {
                        "rich_text": [{"type": "text", "text": {"content": line[2:]}}]
                    }
                })
            # Numbered list
            elif line and line[0].isdigit() and '. ' in line[:4]:
                content = line.split('. ', 1)[1] if '. ' in line else line
                blocks.append({
                    "object": "block",
                    "type": "numbered_list_item",
                    "numbered_list_item": {
                        "rich_text": [{"type": "text", "text": {"content": content}}]
                    }
                })
            # Divider
            elif line.startswith('---'):
                blocks.append({
                    "object": "block",
                    "type": "divider",
                    "divider": {}
                })
            # Regular paragraph
            else:
                # Handle bold and italic
                blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": self._parse_rich_text(line)
                    }
                })

            i += 1

        return blocks

    def _parse_rich_text(self, text: str) -> List[Dict]:
        """
        Parse text with markdown formatting into Notion rich text.

        Args:
            text: Text with markdown formatting

        Returns:
            List of Notion rich text objects
        """
        # Simple implementation - can be enhanced for complex markdown
        if '**' in text or '*' in text or '[' in text:
            # For now, return as plain text
            # A full implementation would parse bold, italic, links, etc.
            return [{"type": "text", "text": {"content": text}}]
        else:
            return [{"type": "text", "text": {"content": text}}]

    def create_daily_summary(self, papers: List[Dict], date: str = None) -> bool:
        """
        Create a daily summary page with all papers.

        Args:
            papers: List of paper summaries
            date: Date string (defaults to today)

        Returns:
            True if successful
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')

        try:
            # Create page content
            blocks = [
                {
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {
                        "rich_text": [{"type": "text", "text": {"content": f"arXiv Papers - {date}"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": f"Found {len(papers)} papers"}}]
                    }
                }
            ]

            properties = {
                "Title": {
                    "title": [
                        {
                            "text": {
                                "content": f"arXiv Daily Summary - {date}"
                            }
                        }
                    ]
                },
                "Published": {
                    "date": {
                        "start": date
                    }
                }
            }

            response = self.client.pages.create(
                parent={"database_id": self.database_id},
                properties=properties,
                children=blocks
            )

            print(f"Created daily summary page for {date}")
            return True

        except Exception as e:
            print(f"Error creating daily summary: {e}")
            return False
