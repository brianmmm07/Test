"""Module for computing paper similarity using embeddings."""
import numpy as np
from typing import List, Dict, Tuple
import re
from collections import Counter
import math

class PaperSimilarity:
    """Compute similarity between academic papers."""

    def __init__(self, use_embeddings: bool = False, anthropic_client=None):
        """
        Initialize similarity calculator.

        Args:
            use_embeddings: Whether to use embeddings (requires additional API calls)
            anthropic_client: Optional Anthropic client for embeddings
        """
        self.use_embeddings = use_embeddings
        self.anthropic_client = anthropic_client

    def compute_embedding(self, paper: Dict) -> List[float]:
        """
        Compute embedding for a paper.

        Args:
            paper: Paper dictionary

        Returns:
            Embedding vector (using TF-IDF if embeddings not available)
        """
        if self.use_embeddings and self.anthropic_client:
            # Use Claude API for embeddings (if available in future)
            # For now, fall back to TF-IDF
            pass

        # Use TF-IDF-like approach for now
        # Combine title (higher weight) and abstract
        text = f"{paper['title']} {paper['title']} {paper['summary']}"
        return self._text_to_vector(text)

    def _text_to_vector(self, text: str, dim: int = 100) -> List[float]:
        """
        Convert text to a fixed-size vector using hash-based approach.

        Args:
            text: Input text
            dim: Vector dimension

        Returns:
            Vector representation
        """
        # Tokenize and clean
        text = text.lower()
        words = re.findall(r'\b\w+\b', text)

        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
            'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'
        }
        words = [w for w in words if w not in stop_words and len(w) > 2]

        # Create vector using hash-based binning
        vector = np.zeros(dim)
        word_counts = Counter(words)

        for word, count in word_counts.items():
            # Use hash to map word to vector index
            idx = hash(word) % dim
            # TF-IDF-like weighting (simplified)
            tf = count / len(words) if words else 0
            vector[idx] += tf

        # Normalize
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm

        return vector.tolist()

    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Compute cosine similarity between two vectors.

        Args:
            vec1: First vector
            vec2: Second vector

        Returns:
            Similarity score (0-1)
        """
        v1 = np.array(vec1)
        v2 = np.array(vec2)

        dot_product = np.dot(v1, v2)
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return float(dot_product / (norm1 * norm2))

    def compute_paper_similarity(self, paper1: Dict, paper2: Dict) -> float:
        """
        Compute similarity between two papers.

        Args:
            paper1: First paper
            paper2: Second paper

        Returns:
            Similarity score (0-1)
        """
        # Check if embeddings are already computed
        emb1 = paper1.get('embedding')
        emb2 = paper2.get('embedding')

        if not emb1:
            emb1 = self.compute_embedding(paper1)
        if not emb2:
            emb2 = self.compute_embedding(paper2)

        similarity = self.cosine_similarity(emb1, emb2)

        # Boost similarity if same category
        if paper1.get('paper_category') == paper2.get('paper_category'):
            similarity = min(1.0, similarity * 1.1)

        # Boost if shared arXiv categories
        cats1 = set(paper1.get('categories', []))
        cats2 = set(paper2.get('categories', []))
        if cats1 & cats2:  # Intersection
            similarity = min(1.0, similarity * 1.05)

        return similarity

    def find_similar_papers(
        self,
        target_paper: Dict,
        candidate_papers: List[Dict],
        top_k: int = 5
    ) -> List[Tuple[Dict, float]]:
        """
        Find top-k most similar papers to a target paper.

        Args:
            target_paper: Paper to find similarities for
            candidate_papers: List of candidate papers
            top_k: Number of similar papers to return

        Returns:
            List of (paper, similarity_score) tuples, sorted by similarity
        """
        similarities = []

        target_emb = target_paper.get('embedding') or self.compute_embedding(target_paper)

        for candidate in candidate_papers:
            # Skip if same paper
            if candidate['id'] == target_paper['id']:
                continue

            cand_emb = candidate.get('embedding') or self.compute_embedding(candidate)
            similarity = self.cosine_similarity(target_emb, cand_emb)

            # Boost for same category
            if candidate.get('paper_category') == target_paper.get('paper_category'):
                similarity = min(1.0, similarity * 1.1)

            # Boost for shared arXiv categories
            cats1 = set(target_paper.get('categories', []))
            cats2 = set(candidate.get('categories', []))
            if cats1 & cats2:
                similarity = min(1.0, similarity * 1.05)

            similarities.append((candidate, similarity))

        # Sort by similarity descending
        similarities.sort(key=lambda x: x[1], reverse=True)

        return similarities[:top_k]

    def detect_shared_benchmarks(self, paper1: Dict, paper2: Dict) -> List[str]:
        """
        Detect if two papers mention the same benchmark datasets.

        Args:
            paper1: First paper
            paper2: Second paper

        Returns:
            List of shared dataset names
        """
        common_datasets = {
            'imagenet', 'coco', 'cifar', 'mnist', 'kinetics', 'ucf101',
            'ActivityNet', 'youtube-8m', 'celeba', 'lsun', 'ade20k',
            'pascal voc', 'cityscapes', 'mscoco', 'openimages', 'laion'
        }

        text1 = (paper1['title'] + ' ' + paper1['summary']).lower()
        text2 = (paper2['title'] + ' ' + paper2['summary']).lower()

        shared = []
        for dataset in common_datasets:
            if dataset in text1 and dataset in text2:
                shared.append(dataset)

        return shared

    def compute_similarity_matrix(
        self,
        papers: List[Dict]
    ) -> np.ndarray:
        """
        Compute pairwise similarity matrix for a list of papers.

        Args:
            papers: List of papers

        Returns:
            NxN similarity matrix
        """
        n = len(papers)
        matrix = np.zeros((n, n))

        # Compute embeddings for all papers
        embeddings = []
        for paper in papers:
            emb = paper.get('embedding') or self.compute_embedding(paper)
            embeddings.append(emb)

        # Compute pairwise similarities
        for i in range(n):
            for j in range(i, n):
                if i == j:
                    matrix[i][j] = 1.0
                else:
                    sim = self.cosine_similarity(embeddings[i], embeddings[j])
                    matrix[i][j] = sim
                    matrix[j][i] = sim

        return matrix
