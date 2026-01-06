"""Module to summarize papers using Claude API."""
import anthropic
from typing import Dict

class PaperSummarizer:
    """Summarizes academic papers using Claude AI."""

    def __init__(self, api_key: str):
        """
        Initialize the summarizer.

        Args:
            api_key: Anthropic API key
        """
        self.client = anthropic.Anthropic(api_key=api_key)

    def summarize_paper(self, paper: Dict) -> str:
        """
        Generate a concise summary of a paper.

        Args:
            paper: Paper dictionary with title, authors, and abstract

        Returns:
            Markdown-formatted summary
        """
        prompt = f"""Please analyze this academic paper and provide a comprehensive summary in markdown format.

Title: {paper['title']}
Authors: {', '.join(paper['authors'][:5])}
Published: {paper['published']}
Category: {paper.get('paper_category', 'General')}

Abstract:
{paper['summary']}

Please provide a structured summary with the following sections:

## Overview
A brief overview (2-3 sentences) of what the paper is about.

## Key Big Picture
The main insight or core idea of this work - what's the key innovation or perspective shift? (2-3 sentences)

## Key Contributions
List 3-5 main contributions or findings as bullet points.

## Methodology
Brief description of the approach or method used (2-3 sentences).

## Key Equations
If the paper presents important mathematical formulations or equations, describe the key ones. If no significant equations, write "No key equations presented" or describe the main technical formulation conceptually.

## Benchmark Results
If the abstract mentions performance metrics, benchmarks, or quantitative results:
- Present key results in a simple markdown table format
- Include dataset names, metrics, and values
- Compare to baselines if mentioned

If no benchmark results are in the abstract, write: "Benchmark results not detailed in abstract - refer to full paper."

## Pros & Cons

**Pros:**
- List 2-3 strengths or advantages of this approach

**Cons:**
- List 2-3 limitations or potential weaknesses (these might be implicit or inferred)

## Potential Impact
How this work could influence the field or be applied (2-3 sentences).

Format everything in clean, well-structured markdown."""

        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=2048,  # Increased for more comprehensive summaries
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            summary = message.content[0].text
            return summary

        except Exception as e:
            print(f"Error summarizing paper '{paper['title']}': {e}")
            return self._create_fallback_summary(paper)

    def _create_fallback_summary(self, paper: Dict) -> str:
        """
        Create a basic summary when API fails.

        Args:
            paper: Paper dictionary

        Returns:
            Basic markdown summary
        """
        authors_str = ", ".join(paper['authors'][:3])
        if len(paper['authors']) > 3:
            authors_str += f" et al."

        return f"""## Overview
This paper titled "{paper['title']}" by {authors_str} was published on {paper['published']}.

## Abstract
{paper['summary'][:500]}{'...' if len(paper['summary']) > 500 else ''}

## Key Big Picture
(Summary generation failed - please refer to the full paper)

## Key Contributions
- Please refer to the full paper for detailed contributions

## Methodology
Please refer to the full paper for methodology details.

## Key Equations
Please refer to the full paper.

## Benchmark Results
Please refer to the full paper.

## Pros & Cons
Please refer to the full paper for analysis.

## Potential Impact
Please refer to the full paper.
"""

    def create_markdown_summary(self, paper: Dict, summary: str, similar_papers: list = None) -> str:
        """
        Create a complete markdown document for a paper.

        Args:
            paper: Paper dictionary
            summary: Generated summary
            similar_papers: List of (paper_dict, similarity_score) tuples

        Returns:
            Complete markdown document
        """
        authors_str = ", ".join(paper['authors'][:5])
        if len(paper['authors']) > 5:
            authors_str += f" et al. ({len(paper['authors'])} authors)"

        # Get category classification
        paper_category = paper.get('paper_category', 'General')

        markdown = f"""# {paper['title']}

**Authors:** {authors_str}
**Published:** {paper['published']}
**Category:** {paper_category}
**arXiv Category:** {paper['primary_category']}
**Search Keyword:** {paper['keyword']}
**PDF:** [{paper['id']}]({paper['pdf_url']})

---

{summary}

---
"""

        # Add related papers section if available
        if similar_papers:
            markdown += "\n## 🔗 Related Papers\n\n"
            markdown += "Based on content similarity, here are the most related papers:\n\n"

            for i, (similar_paper, score) in enumerate(similar_papers, 1):
                similarity_pct = int(score * 100)
                similar_authors = ", ".join(similar_paper['authors'][:3])
                if len(similar_paper['authors']) > 3:
                    similar_authors += " et al."

                markdown += f"{i}. **{similar_paper['title']}**\n"
                markdown += f"   - Authors: {similar_authors}\n"
                markdown += f"   - Published: {similar_paper['published']}\n"
                markdown += f"   - Similarity: {similarity_pct}%\n"
                markdown += f"   - [PDF]({similar_paper['pdf_url']})\n\n"

            markdown += "---\n\n"

        markdown += "*Summary generated by Claude AI*\n"

        return markdown
