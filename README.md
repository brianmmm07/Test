# arXiv Paper Summarizer with Notion Integration

Automatically fetch, summarize, and send arXiv papers to your Notion database daily. This tool searches for papers based on your specified keywords (e.g., "image generation", "video generation"), generates AI-powered summaries using Claude, and organizes them in Notion.

## Features

- 🔍 **Keyword-based Search**: Automatically search arXiv for papers matching your keywords
- 🤖 **AI Summarization**: Generate concise, structured summaries using Claude AI
- 📝 **Notion Integration**: Automatically add papers to your Notion database
- ⏰ **Daily Scheduling**: Run automatically at a scheduled time each day
- 🎯 **Customizable**: Configure keywords, number of papers, and schedule

## Prerequisites

- Python 3.8 or higher
- Anthropic API key (for Claude AI)
- Notion integration token and database ID

## Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd Test
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up Notion

#### Create a Notion Integration

1. Go to [Notion Integrations](https://www.notion.so/my-integrations)
2. Click "New integration"
3. Name it (e.g., "arXiv Summarizer")
4. Select the workspace
5. Copy the "Internal Integration Token"

#### Create a Database

1. Create a new database in Notion (full page)
2. Add the following properties:
   - **Title** (Title) - Default property
   - **Authors** (Text)
   - **Published** (Date)
   - **Category** (Select) - Your custom categories (e.g., Image Generation, Video Generation)
   - **arXiv Category** (Select) - arXiv's classification (e.g., cs.CV, cs.AI)
   - **Keywords** (Multi-select)
   - **URL** (URL)

3. Share the database with your integration:
   - Click "..." menu in top right
   - Click "Add connections"
   - Select your integration

4. Copy the database ID from the URL:
   ```
   https://notion.so/your-workspace/DATABASE_ID?v=...
   ```

### 4. Get Anthropic API Key

1. Go to [Anthropic Console](https://console.anthropic.com/)
2. Create an account or sign in
3. Navigate to API Keys
4. Create a new API key
5. Copy the key

### 5. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` and fill in your credentials:

```env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
NOTION_TOKEN=your_notion_integration_token_here
NOTION_DATABASE_ID=your_notion_database_id_here

# Categorized keywords (recommended):
KEYWORDS=Image Generation: image generation, diffusion model, image editing | Video Generation: video generation, video extension, motion synthesis

# Or simple format:
# KEYWORDS=image generation,video generation,diffusion models

MAX_PAPERS_PER_KEYWORD=5
SCHEDULE_TIME=09:00
```

## 🚀 Quick Deploy (Recommended)

**Want to run this automatically without managing servers?**

### GitHub Actions (FREE) - Best Option
1. Push this repo to GitHub
2. Add your API keys as GitHub Secrets
3. It runs automatically every day!

👉 **[See Full Deployment Guide](DEPLOYMENT.md)** for GitHub Actions, Railway, Render, Docker, and AWS Lambda options.

---

## Usage

### Run Locally Once

To run the summarizer immediately:

```bash
python main.py
```

This will:
1. Fetch recent papers from arXiv based on your keywords
2. Generate summaries using Claude AI
3. Add them to your Notion database

### Run with Scheduler

To run the summarizer daily at a scheduled time:

```bash
python scheduler.py
```

This will:
1. Run an initial summary immediately
2. Schedule daily runs at the time specified in `SCHEDULE_TIME`
3. Continue running until you press Ctrl+C

### Run as Background Service (Linux/Mac)

For production use, consider running with `screen` or `tmux`:

```bash
# Using screen
screen -S arxiv-summarizer
python scheduler.py
# Press Ctrl+A then D to detach

# Reattach later with:
screen -r arxiv-summarizer
```

Or use a systemd service (create `/etc/systemd/system/arxiv-summarizer.service`):

```ini
[Unit]
Description=arXiv Paper Summarizer
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/Test
Environment=PATH=/usr/bin:/usr/local/bin
ExecStart=/usr/bin/python3 scheduler.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable arxiv-summarizer
sudo systemctl start arxiv-summarizer
```

## Configuration Options

Edit `.env` to customize:

- **KEYWORDS**: Search keywords - supports two formats:
  - **Categorized (recommended)**: Organize papers by category in Notion
    - Format: `Category1: keyword1, keyword2 | Category2: keyword3, keyword4`
    - Example: `Image Generation: image generation, diffusion model | Video Generation: video generation, motion synthesis`
    - Papers matching multiple categories are assigned to the first matching category
  - **Simple**: `keyword1, keyword2, keyword3` (creates single "General" category)

- **MAX_PAPERS_PER_KEYWORD**: Maximum papers to fetch per keyword (default: 5)
- **SCHEDULE_TIME**: Time to run daily in 24-hour format (e.g., "09:00")

### Category Organization

When using categorized keywords:
- Papers are organized by your custom categories in Notion's **Category** field
- If a paper matches multiple categories, it's placed in the first matching category
- The **arXiv Category** field preserves arXiv's original classification (e.g., cs.CV, cs.AI)
- This allows you to filter and view papers in Notion by your research interests

## Project Structure

```
Test/
├── main.py                          # Main application logic
├── scheduler.py                     # Daily scheduling
├── arxiv_fetcher.py                 # arXiv API integration
├── summarizer.py                    # Claude AI summarization
├── notion_client.py                 # Notion API integration
├── config.py                        # Configuration management
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment template
├── .github/workflows/               # GitHub Actions for auto-deployment
│   └── daily-summarizer.yml
├── Dockerfile                       # Docker containerization
├── docker-compose.yml               # Docker Compose config
├── DEPLOYMENT.md                    # Deployment guide
└── README.md                        # This file
```

## How It Works

1. **Fetch Papers**: Uses the arXiv API to search for recent papers matching your keywords
2. **Summarize**: Sends each paper's abstract to Claude AI for intelligent summarization
3. **Format**: Creates structured markdown summaries with key insights
4. **Send to Notion**: Adds each paper as a new page in your Notion database

## Troubleshooting

### "Missing required environment variables"

Make sure your `.env` file exists and contains all required keys:
- ANTHROPIC_API_KEY
- NOTION_TOKEN
- NOTION_DATABASE_ID

### "Error accessing database"

1. Verify your database ID is correct
2. Ensure the database is shared with your Notion integration
3. Check that all required properties exist in the database

### "No new papers found"

- Try broadening your keywords
- Check that arXiv has recent papers in your search area
- Increase `MAX_PAPERS_PER_KEYWORD`

### Rate Limits

- arXiv API: Respectful rate limiting (3 seconds between requests)
- Anthropic API: Check your plan's rate limits
- Notion API: 3 requests per second limit

## Customization

### Change Summary Format

Edit `summarizer.py` and modify the prompt in `summarize_paper()` to customize how papers are summarized.

### Add More Notion Properties

Edit `notion_client.py` in the `add_paper()` method to add custom properties to your database.

### Filter by Date Range

Modify `arxiv_fetcher.py` and adjust the `days_back` parameter in `fetch_recent_papers()`.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - feel free to use this project for any purpose.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the code comments
3. Open an issue on GitHub

---

**Note**: This tool is for research and educational purposes. Please respect arXiv's terms of service and API usage guidelines.
