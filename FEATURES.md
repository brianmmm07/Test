# Paper Database and Similarity Features

This document describes the advanced features for paper management, similarity tracking, and search functionality.

## Overview

The arXiv Paper Summarizer now includes a local database system that:
- Stores all papers permanently for fast search and reference
- Computes similarity between papers using text embeddings
- Finds and displays top-5 most similar papers for each new paper
- Enables search by author, date, category, and similarity
- Maintains organized metadata for proper indexing

## Features

### 1. Local Paper Database

All papers are stored in a local SQLite database (`papers.db`) with:
- **Full metadata**: Title, authors, abstract, publication date, categories
- **Paper embeddings**: Vector representations for similarity computation
- **Notion integration**: Links to corresponding Notion pages
- **Fast indexing**: Optimized for searches by date, author, and category

### 2. Similarity Tracking

#### How It Works
- Each paper is converted to a vector embedding based on title and abstract
- Similarity is computed using cosine similarity between embeddings
- Papers in the same category receive a similarity boost
- Papers sharing arXiv categories receive additional boost
- Top-5 most similar papers are identified for each new paper

#### Similarity Score
- Score ranges from 0% to 100%
- Higher scores indicate more similar content
- Considers:
  - Content similarity (title + abstract)
  - Category matching
  - Shared research areas

### 3. Related Papers in Notion

When a new paper is added to Notion, it automatically includes:
- **🔗 Related Papers section**
- List of top-5 most similar papers with:
  - Title and authors
  - Publication date
  - Similarity percentage
  - Direct link to PDF

Example:
```markdown
## 🔗 Related Papers

Based on content similarity, here are the most related papers:

1. **Attention Is All You Need**
   - Authors: Vaswani et al.
   - Published: 2017-06-12
   - Similarity: 85%
   - [PDF](https://arxiv.org/pdf/1706.03762.pdf)

2. **BERT: Pre-training of Deep Bidirectional Transformers**
   - Authors: Devlin et al.
   - Published: 2018-10-11
   - Similarity: 78%
   - [PDF](https://arxiv.org/pdf/1810.04805.pdf)
```

### 4. Search Functionality

Use the `search.py` command-line tool to query your paper database.

#### Search by Author

Find all papers by a specific author:
```bash
python search.py --author "Geoffrey Hinton"
python search.py --author "Yann LeCun"
```

#### Search by Date Range

Find papers within a date range:
```bash
python search.py --date-range 2024-01-01 2024-12-31
python search.py --date-range 2023-06-01 2023-12-31
```

#### Search by Category

Find papers in a specific category:
```bash
python search.py --category "Image Generation"
python search.py --category "Video Generation"
```

#### Find Similar Papers

Find papers similar to a given paper:
```bash
# Using full URL
python search.py --similar "http://arxiv.org/abs/2401.12345"

# Using just the ID
python search.py --similar "2401.12345"
```

This will show:
- The target paper details
- Top 10 most similar papers
- Similarity scores for each

#### List Recent Papers

See the most recently added papers:
```bash
python search.py --recent 20  # Show 20 most recent
python search.py --recent 50  # Show 50 most recent
```

#### Database Statistics

View overall database statistics:
```bash
python search.py --stats
```

Shows:
- Total number of papers
- Papers per category
- Date range of papers
- Number of similarity connections

### 5. Database Schema

The database consists of three main tables:

#### Papers Table
- `id`: arXiv paper ID (primary key)
- `title`: Paper title
- `authors`: JSON array of author names
- `summary`: Abstract text
- `published_date`: Publication date
- `pdf_url`: Link to PDF
- `primary_category`: arXiv category (e.g., cs.CV)
- `paper_category`: Custom category (e.g., Image Generation)
- `keyword`: Search keyword that found this paper
- `embedding`: JSON array of embedding vector
- `added_date`: When added to database
- `notion_page_id`: Corresponding Notion page ID

#### Paper Similarities Table
- `paper_id`: First paper ID
- `related_paper_id`: Related paper ID
- `similarity_score`: Similarity score (0-1)
- Bidirectional relationships for fast queries

#### Benchmarks Table (Future Use)
- `paper_id`: Paper ID
- `dataset_name`: Dataset mentioned (e.g., ImageNet, COCO)
- `metric_name`: Performance metric
- `metric_value`: Metric value

## Usage Examples

### Daily Workflow

1. **Run the summarizer** to fetch new papers:
   ```bash
   python main.py
   ```

2. **View similar papers** in Notion automatically

3. **Search for specific papers**:
   ```bash
   python search.py --author "Ilya Sutskever"
   ```

4. **Check database stats**:
   ```bash
   python search.py --stats
   ```

### Example: Finding Related Research

If you're interested in papers related to a specific work:

```bash
# Find papers similar to "Stable Diffusion"
python search.py --similar "2112.10752"
```

This shows you the research landscape around that paper, helping you:
- Discover related work
- Track research evolution
- Find papers using similar techniques
- Identify key researchers in the area

### Example: Tracking Author Output

Monitor papers from specific researchers:

```bash
# All papers by Andrew Ng in database
python search.py --author "Andrew Ng"

# Recent papers in Image Generation category
python search.py --category "Image Generation"
```

## Implementation Details

### Embedding Generation

Papers are embedded using a hash-based TF-IDF approach:
1. Combine title (2x weight) and abstract
2. Tokenize and remove stop words
3. Compute term frequencies
4. Map to fixed-size vector (100 dimensions)
5. Normalize vector

Future versions may use Claude embeddings for better similarity.

### Similarity Computation

Similarity is computed as:
```
base_similarity = cosine_similarity(embedding1, embedding2)

if same_category:
    similarity *= 1.1  # 10% boost

if shared_arxiv_categories:
    similarity *= 1.05  # 5% boost

final_similarity = min(1.0, similarity)
```

### Performance

- Database queries are optimized with indexes
- Similarity computation is fast (milliseconds)
- Embedding computation is one-time per paper
- Search scales to thousands of papers

## Database Maintenance

### Backup

The database is in `papers.db`. To backup:
```bash
cp papers.db papers_backup_$(date +%Y%m%d).db
```

### Reset

To start fresh:
```bash
rm papers.db
python main.py  # Will create new database
```

### Export

Papers are also in Notion, which provides automatic backup.

## Advanced Features

### Category Organization

Papers are automatically organized by:
- **Custom categories**: Your research categories (Image Generation, etc.)
- **arXiv categories**: Official arXiv classification (cs.CV, cs.AI, etc.)
- **Keywords**: Which search term found the paper
- **Date**: Publication date for chronological tracking

### Duplicate Prevention

- Papers are identified by unique arXiv ID
- If a paper matches multiple keywords, it's added once
- Assigned to the first matching category
- Similarity relationships prevent redundant processing

### Scalability

The system is designed to handle:
- Thousands of papers in database
- Fast similarity searches
- Efficient date/author queries
- Growing collection over time

## Future Enhancements

Potential improvements:
- **Better embeddings**: Use Claude API for semantic embeddings
- **Benchmark tracking**: Extract and compare performance metrics
- **Citation analysis**: Track citation relationships
- **Trend detection**: Identify emerging research trends
- **Collaborative filtering**: Recommend papers based on interests
- **Web interface**: Browse and search via web UI

## Troubleshooting

### Database is slow
- Check database size: `ls -lh papers.db`
- Consider periodic cleanup of old papers
- Indexes are automatically maintained

### Similarity scores seem off
- Ensure embeddings are being computed
- Check that papers have full abstracts
- Category boosts may need tuning

### Search returns no results
- Verify database has papers: `python search.py --stats`
- Check date format: YYYY-MM-DD
- Author names must match exactly (partial matching supported)

## Integration with Notion

### Notion Database Schema

Your Notion database should have:
- **Title** (Title)
- **Authors** (Text)
- **Published** (Date)
- **Category** (Select) - Your custom categories
- **arXiv Category** (Select) - arXiv's classification
- **Keywords** (Multi-select)
- **URL** (URL)

### Related Papers Display

Related papers are shown in each Notion page as:
- Formatted list with similarity percentages
- Clickable links to PDFs
- Author names and publication dates
- Easy to scan and reference

## Best Practices

1. **Run daily** to keep database current
2. **Check stats** periodically to monitor growth
3. **Use categories** to organize by research area
4. **Search similar** when diving into a new topic
5. **Track authors** you frequently cite
6. **Export backups** of your database monthly

## Summary

The paper database and similarity system provides:
- ✅ Permanent storage of all papers
- ✅ Automatic similarity detection
- ✅ Top-5 related papers for each new paper
- ✅ Search by author, date, category, similarity
- ✅ Organized metadata for proper indexing
- ✅ Integration with Notion
- ✅ Fast, scalable queries

This transforms the arXiv summarizer from a simple fetcher into a comprehensive research management system.
