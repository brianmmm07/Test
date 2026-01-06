"""Module for managing local paper database with similarity tracking."""
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Tuple, Optional
import os

class PaperDatabase:
    """Manages local SQLite database of papers with similarity tracking."""

    def __init__(self, db_path: str = "papers.db"):
        """
        Initialize paper database.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.conn = None
        self._init_database()

    def _init_database(self):
        """Initialize database schema."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        cursor = self.conn.cursor()

        # Papers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS papers (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                authors TEXT NOT NULL,  -- JSON array
                summary TEXT,
                published_date DATE NOT NULL,
                pdf_url TEXT,
                primary_category TEXT,
                paper_category TEXT,
                keyword TEXT,
                embedding TEXT,  -- JSON array of floats
                added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notion_page_id TEXT
            )
        ''')

        # Paper similarities table (many-to-many relationships)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS paper_similarities (
                paper_id TEXT NOT NULL,
                related_paper_id TEXT NOT NULL,
                similarity_score REAL NOT NULL,
                PRIMARY KEY (paper_id, related_paper_id),
                FOREIGN KEY (paper_id) REFERENCES papers(id),
                FOREIGN KEY (related_paper_id) REFERENCES papers(id)
            )
        ''')

        # Benchmarks table (for tracking papers using same datasets)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS benchmarks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                paper_id TEXT NOT NULL,
                dataset_name TEXT NOT NULL,
                metric_name TEXT,
                metric_value REAL,
                FOREIGN KEY (paper_id) REFERENCES papers(id)
            )
        ''')

        # Create indexes for faster searching
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_published_date
            ON papers(published_date DESC)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_paper_category
            ON papers(paper_category)
        ''')

        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_similarity_score
            ON paper_similarities(similarity_score DESC)
        ''')

        self.conn.commit()

    def add_paper(self, paper: Dict, embedding: List[float] = None, notion_page_id: str = None) -> bool:
        """
        Add a paper to the database.

        Args:
            paper: Paper dictionary
            embedding: Paper embedding vector
            notion_page_id: Notion page ID if created

        Returns:
            True if added, False if already exists
        """
        cursor = self.conn.cursor()

        # Check if paper already exists
        cursor.execute('SELECT id FROM papers WHERE id = ?', (paper['id'],))
        if cursor.fetchone():
            return False

        # Insert paper
        cursor.execute('''
            INSERT INTO papers (
                id, title, authors, summary, published_date,
                pdf_url, primary_category, paper_category, keyword,
                embedding, notion_page_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            paper['id'],
            paper['title'],
            json.dumps(paper['authors']),
            paper['summary'],
            paper['published'],
            paper['pdf_url'],
            paper['primary_category'],
            paper.get('paper_category', 'General'),
            paper['keyword'],
            json.dumps(embedding) if embedding else None,
            notion_page_id
        ))

        self.conn.commit()
        return True

    def get_paper(self, paper_id: str) -> Optional[Dict]:
        """Get a paper by ID."""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM papers WHERE id = ?', (paper_id,))
        row = cursor.fetchone()

        if not row:
            return None

        paper = dict(row)
        paper['authors'] = json.loads(paper['authors'])
        if paper['embedding']:
            paper['embedding'] = json.loads(paper['embedding'])

        return paper

    def add_similarity(self, paper_id: str, related_id: str, score: float):
        """
        Add similarity relationship between two papers.

        Args:
            paper_id: First paper ID
            related_id: Related paper ID
            score: Similarity score (0-1)
        """
        cursor = self.conn.cursor()

        # Add bidirectional relationship
        cursor.execute('''
            INSERT OR REPLACE INTO paper_similarities
            (paper_id, related_paper_id, similarity_score)
            VALUES (?, ?, ?)
        ''', (paper_id, related_id, score))

        cursor.execute('''
            INSERT OR REPLACE INTO paper_similarities
            (paper_id, related_paper_id, similarity_score)
            VALUES (?, ?, ?)
        ''', (related_id, paper_id, score))

        self.conn.commit()

    def get_similar_papers(self, paper_id: str, top_k: int = 5) -> List[Tuple[Dict, float]]:
        """
        Get top-k most similar papers.

        Args:
            paper_id: Paper ID to find similarities for
            top_k: Number of similar papers to return

        Returns:
            List of (paper_dict, similarity_score) tuples
        """
        cursor = self.conn.cursor()

        cursor.execute('''
            SELECT p.*, ps.similarity_score
            FROM papers p
            JOIN paper_similarities ps ON p.id = ps.related_paper_id
            WHERE ps.paper_id = ?
            ORDER BY ps.similarity_score DESC
            LIMIT ?
        ''', (paper_id, top_k))

        results = []
        for row in cursor.fetchall():
            paper = dict(row)
            similarity = paper.pop('similarity_score')
            paper['authors'] = json.loads(paper['authors'])
            if paper['embedding']:
                paper['embedding'] = json.loads(paper['embedding'])
            results.append((paper, similarity))

        return results

    def search_by_author(self, author_name: str) -> List[Dict]:
        """
        Search papers by author name.

        Args:
            author_name: Author name to search for

        Returns:
            List of matching papers
        """
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM papers
            WHERE authors LIKE ?
            ORDER BY published_date DESC
        ''', (f'%{author_name}%',))

        results = []
        for row in cursor.fetchall():
            paper = dict(row)
            paper['authors'] = json.loads(paper['authors'])
            if paper['embedding']:
                paper['embedding'] = json.loads(paper['embedding'])
            results.append(paper)

        return results

    def search_by_date_range(self, start_date: str, end_date: str) -> List[Dict]:
        """
        Search papers by date range.

        Args:
            start_date: Start date (YYYY-MM-DD)
            end_date: End date (YYYY-MM-DD)

        Returns:
            List of papers in date range
        """
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM papers
            WHERE published_date BETWEEN ? AND ?
            ORDER BY published_date DESC
        ''', (start_date, end_date))

        results = []
        for row in cursor.fetchall():
            paper = dict(row)
            paper['authors'] = json.loads(paper['authors'])
            if paper['embedding']:
                paper['embedding'] = json.loads(paper['embedding'])
            results.append(paper)

        return results

    def get_papers_by_category(self, category: str) -> List[Dict]:
        """Get all papers in a category."""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM papers
            WHERE paper_category = ?
            ORDER BY published_date DESC
        ''', (category,))

        results = []
        for row in cursor.fetchall():
            paper = dict(row)
            paper['authors'] = json.loads(paper['authors'])
            if paper['embedding']:
                paper['embedding'] = json.loads(paper['embedding'])
            results.append(paper)

        return results

    def get_all_papers(self, limit: int = None) -> List[Dict]:
        """
        Get all papers in database.

        Args:
            limit: Optional limit on number of papers

        Returns:
            List of all papers
        """
        cursor = self.conn.cursor()

        if limit:
            cursor.execute('''
                SELECT * FROM papers
                ORDER BY published_date DESC
                LIMIT ?
            ''', (limit,))
        else:
            cursor.execute('SELECT * FROM papers ORDER BY published_date DESC')

        results = []
        for row in cursor.fetchall():
            paper = dict(row)
            paper['authors'] = json.loads(paper['authors'])
            if paper['embedding']:
                paper['embedding'] = json.loads(paper['embedding'])
            results.append(paper)

        return results

    def get_statistics(self) -> Dict:
        """Get database statistics."""
        cursor = self.conn.cursor()

        stats = {}

        # Total papers
        cursor.execute('SELECT COUNT(*) as count FROM papers')
        stats['total_papers'] = cursor.fetchone()['count']

        # Papers by category
        cursor.execute('''
            SELECT paper_category, COUNT(*) as count
            FROM papers
            GROUP BY paper_category
        ''')
        stats['papers_by_category'] = {row['paper_category']: row['count']
                                       for row in cursor.fetchall()}

        # Date range
        cursor.execute('''
            SELECT MIN(published_date) as earliest, MAX(published_date) as latest
            FROM papers
        ''')
        row = cursor.fetchone()
        stats['date_range'] = {
            'earliest': row['earliest'],
            'latest': row['latest']
        }

        # Total similarities computed
        cursor.execute('SELECT COUNT(*) as count FROM paper_similarities')
        stats['total_similarities'] = cursor.fetchone()['count'] // 2  # Bidirectional

        return stats

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
