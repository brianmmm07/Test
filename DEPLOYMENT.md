# Deployment Guide

This guide covers multiple ways to run the arXiv Paper Summarizer automatically every day without running it locally.

## Table of Contents
1. [GitHub Actions (Recommended - FREE)](#1-github-actions-recommended)
2. [Railway (Simple Deployment)](#2-railway)
3. [Render (Free Tier Available)](#3-render)
4. [Docker on Any VPS](#4-docker-on-vps)
5. [AWS Lambda](#5-aws-lambda)

---

## 1. GitHub Actions (Recommended)

**Cost:** FREE (2000 minutes/month free tier)
**Setup Time:** 5 minutes
**Difficulty:** Easy ⭐

### Advantages
- ✅ Completely free for public repos
- ✅ No server management required
- ✅ Built-in secret management
- ✅ Easy to monitor runs
- ✅ Manual trigger option

### Setup Instructions

#### Step 1: Push to GitHub
```bash
git push origin claude/arxiv-summarizer-notion-5mCuv
```

#### Step 2: Add Secrets to GitHub
1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add these secrets:

| Secret Name | Value |
|------------|-------|
| `ANTHROPIC_API_KEY` | Your Anthropic API key |
| `NOTION_TOKEN` | Your Notion integration token |
| `NOTION_DATABASE_ID` | Your Notion database ID |
| `KEYWORDS` | `image generation,video generation` (or your keywords) |
| `MAX_PAPERS_PER_KEYWORD` | `5` (optional, defaults to 5) |

#### Step 3: Enable GitHub Actions
1. Go to the **Actions** tab in your repository
2. Enable workflows if prompted
3. You should see "Daily arXiv Paper Summarizer" workflow

#### Step 4: Test Manual Run
1. Go to **Actions** tab
2. Click on "Daily arXiv Paper Summarizer"
3. Click **Run workflow** → **Run workflow**
4. Watch it execute!

#### Step 5: Configure Schedule
The workflow runs daily at 9:00 AM UTC by default.

To change the time, edit `.github/workflows/daily-summarizer.yml`:
```yaml
schedule:
  - cron: '0 9 * * *'  # Change '9' to your desired hour (UTC)
```

**Cron examples:**
- `0 9 * * *` - 9:00 AM UTC daily
- `30 14 * * *` - 2:30 PM UTC daily
- `0 0 * * *` - Midnight UTC daily
- `0 */6 * * *` - Every 6 hours

#### Monitoring
- View logs: **Actions** tab → Click on a workflow run
- Get email notifications: Settings → Notifications → Actions

---

## 2. Railway

**Cost:** $5/month after free trial
**Setup Time:** 10 minutes
**Difficulty:** Easy ⭐⭐

### Setup Instructions

#### Step 1: Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub

#### Step 2: Deploy
1. Click **New Project** → **Deploy from GitHub repo**
2. Select your repository
3. Railway will auto-detect Python

#### Step 3: Add Environment Variables
In Railway dashboard:
- Click on your service
- Go to **Variables** tab
- Add all variables from `.env.example`

#### Step 4: Configure
Railway will run `scheduler.py` automatically. To customize:
1. Add a `Procfile`:
```
worker: python scheduler.py
```

#### Advantages
- Simple deployment
- Auto-deploys on git push
- Good monitoring dashboard

---

## 3. Render

**Cost:** FREE tier available (with limitations)
**Setup Time:** 10 minutes
**Difficulty:** Easy ⭐⭐

### Setup Instructions

#### Step 1: Create Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub

#### Step 2: Create Background Worker
1. Click **New** → **Background Worker**
2. Connect your GitHub repository
3. Configure:
   - **Name:** arxiv-summarizer
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python scheduler.py`

#### Step 3: Add Environment Variables
In the Render dashboard, add all your secrets from `.env.example`

#### Step 4: Deploy
Click **Create Background Worker**

#### Monitoring
- View logs in real-time from Render dashboard
- Set up health checks and alerts

---

## 4. Docker on VPS

**Cost:** $5-6/month (DigitalOcean, Linode, Vultr)
**Setup Time:** 20 minutes
**Difficulty:** Medium ⭐⭐⭐

### Setup Instructions

#### Step 1: Get a VPS
Popular options:
- [DigitalOcean](https://digitalocean.com) - $6/month
- [Linode](https://linode.com) - $5/month
- [Vultr](https://vultr.com) - $5/month

Choose Ubuntu 22.04 LTS

#### Step 2: Install Docker
```bash
ssh root@your-vps-ip

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt-get install docker-compose-plugin
```

#### Step 3: Clone Repository
```bash
git clone https://github.com/yourusername/Test.git
cd Test
```

#### Step 4: Configure Environment
```bash
cp .env.example .env
nano .env  # Edit with your credentials
```

#### Step 5: Run with Docker Compose
```bash
docker compose up -d
```

#### Step 6: Verify
```bash
docker compose logs -f  # Watch logs
```

#### Management Commands
```bash
# Stop
docker compose down

# Restart
docker compose restart

# View logs
docker compose logs -f

# Update code
git pull
docker compose up -d --build
```

---

## 5. AWS Lambda

**Cost:** ~$0-1/month
**Setup Time:** 30 minutes
**Difficulty:** Hard ⭐⭐⭐⭐

### Setup Overview

This is more complex but very cost-effective for scheduled tasks.

#### Requirements
- AWS Account
- AWS CLI installed
- Knowledge of CloudFormation or Serverless Framework

#### High-Level Steps
1. Package application with dependencies as Lambda layer
2. Create Lambda function
3. Set up EventBridge (CloudWatch Events) for scheduling
4. Configure environment variables in Lambda
5. Set up CloudWatch Logs for monitoring

#### Using Serverless Framework

Create `serverless.yml`:
```yaml
service: arxiv-summarizer

provider:
  name: aws
  runtime: python3.11
  region: us-east-1
  environment:
    ANTHROPIC_API_KEY: ${env:ANTHROPIC_API_KEY}
    NOTION_TOKEN: ${env:NOTION_TOKEN}
    NOTION_DATABASE_ID: ${env:NOTION_DATABASE_ID}

functions:
  daily:
    handler: lambda_handler.handler
    events:
      - schedule: cron(0 9 * * ? *)  # 9 AM UTC daily
    timeout: 900  # 15 minutes
```

Create `lambda_handler.py`:
```python
from main import run_daily_summary

def handler(event, context):
    run_daily_summary()
    return {"statusCode": 200, "body": "Success"}
```

Deploy:
```bash
serverless deploy
```

---

## Comparison Table

| Solution | Cost/Month | Difficulty | Auto-Updates | Monitoring |
|----------|-----------|------------|--------------|------------|
| **GitHub Actions** | **FREE** | ⭐ Easy | ✅ Yes | ✅ Good |
| Railway | $5 | ⭐⭐ Easy | ✅ Yes | ✅ Excellent |
| Render | Free tier | ⭐⭐ Easy | ✅ Yes | ✅ Good |
| Docker VPS | $5-6 | ⭐⭐⭐ Medium | ⚠️ Manual | ⚠️ Manual |
| AWS Lambda | ~$0.50 | ⭐⭐⭐⭐ Hard | ⚠️ Manual | ✅ CloudWatch |

---

## Recommended Choice

### For Most Users: **GitHub Actions**
- Free and reliable
- Easy to set up
- Great for scheduled tasks
- No server management

### For 24/7 Services: **Railway or Render**
- If you need the app running continuously (not just daily)
- Good dashboards and logging
- Auto-deployment on push

### For Cost Optimization: **AWS Lambda**
- If you're comfortable with AWS
- Best cost for infrequent runs
- Scales automatically

---

## Troubleshooting

### GitHub Actions Not Running
1. Check if Actions are enabled: **Settings** → **Actions** → **General**
2. Verify secrets are set correctly
3. Check workflow syntax with: `yamllint .github/workflows/daily-summarizer.yml`

### Docker Container Exits
```bash
# Check logs
docker compose logs

# Common issues:
# - Missing .env file
# - Invalid API keys
# - Wrong timezone
```

### Railway/Render Not Working
- Ensure environment variables are set
- Check logs in dashboard
- Verify Python version compatibility

---

## Monitoring Best Practices

### Set Up Notifications
1. **GitHub Actions:** Settings → Notifications
2. **Railway/Render:** Configure webhooks to Slack/Discord
3. **Docker:** Set up a cron job to check container health

### Health Checks
Add to `main.py`:
```python
# Send notification if no papers found for 3 days
# Send alert if Notion API fails
# Log summary statistics
```

### Backup Strategy
- Papers are in Notion (backed up by Notion)
- Logs in GitHub Actions artifacts (7 days retention)
- Consider exporting Notion database weekly

---

## Support

For deployment issues:
- GitHub Actions: Check [Actions documentation](https://docs.github.com/en/actions)
- Railway: [Railway docs](https://docs.railway.app)
- Render: [Render docs](https://render.com/docs)
- Docker: [Docker docs](https://docs.docker.com)

For application issues, check the main README.md
