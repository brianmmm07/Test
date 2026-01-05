#!/bin/bash

# Helper script to set up GitHub Actions secrets
# This script generates the commands you need to run to add secrets

echo "========================================="
echo "GitHub Actions Setup Helper"
echo "========================================="
echo ""
echo "To deploy with GitHub Actions, you need to add secrets to your repository."
echo ""
echo "Follow these steps:"
echo ""
echo "1. Push this repository to GitHub if you haven't already:"
echo "   git push origin main"
echo ""
echo "2. Go to your GitHub repository"
echo "3. Click: Settings → Secrets and variables → Actions"
echo "4. Click: New repository secret"
echo ""
echo "5. Add these secrets one by one:"
echo ""

# Check if .env exists
if [ -f .env ]; then
    source .env

    echo "   Secret: ANTHROPIC_API_KEY"
    if [ ! -z "$ANTHROPIC_API_KEY" ]; then
        echo "   Value:  $ANTHROPIC_API_KEY"
    else
        echo "   Value:  <your Anthropic API key>"
    fi
    echo ""

    echo "   Secret: NOTION_TOKEN"
    if [ ! -z "$NOTION_TOKEN" ]; then
        echo "   Value:  $NOTION_TOKEN"
    else
        echo "   Value:  <your Notion integration token>"
    fi
    echo ""

    echo "   Secret: NOTION_DATABASE_ID"
    if [ ! -z "$NOTION_DATABASE_ID" ]; then
        echo "   Value:  $NOTION_DATABASE_ID"
    else
        echo "   Value:  <your Notion database ID>"
    fi
    echo ""

    echo "   Secret: KEYWORDS"
    if [ ! -z "$KEYWORDS" ]; then
        echo "   Value:  $KEYWORDS"
    else
        echo "   Value:  image generation,video generation"
    fi
    echo ""

    echo "   Secret: MAX_PAPERS_PER_KEYWORD (optional)"
    if [ ! -z "$MAX_PAPERS_PER_KEYWORD" ]; then
        echo "   Value:  $MAX_PAPERS_PER_KEYWORD"
    else
        echo "   Value:  5"
    fi
    echo ""
else
    echo "   ⚠️  .env file not found. Here are the secrets you need to add:"
    echo ""
    echo "   - ANTHROPIC_API_KEY"
    echo "   - NOTION_TOKEN"
    echo "   - NOTION_DATABASE_ID"
    echo "   - KEYWORDS (e.g., image generation,video generation)"
    echo "   - MAX_PAPERS_PER_KEYWORD (optional, default: 5)"
    echo ""
fi

echo "========================================="
echo "After adding secrets:"
echo "========================================="
echo ""
echo "1. Go to the Actions tab in your repository"
echo "2. Enable workflows if prompted"
echo "3. Click on 'Daily arXiv Paper Summarizer'"
echo "4. Click 'Run workflow' to test it manually"
echo ""
echo "The workflow will then run automatically every day at 9:00 AM UTC"
echo ""
echo "To change the schedule, edit:"
echo "  .github/workflows/daily-summarizer.yml"
echo ""
echo "For more deployment options, see:"
echo "  DEPLOYMENT.md"
echo ""
