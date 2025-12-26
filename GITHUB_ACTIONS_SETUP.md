# GitHub Actions Setup Guide

## Setting up the Vacation Scheme Search on GitHub Actions

### 1. Push your code to GitHub
```bash
git add .
git commit -m "Add vacation scheme search agent"
git push
```

### 2. Configure GitHub Secrets

Go to your repository on GitHub, then navigate to:
**Settings → Secrets and variables → Actions → New repository secret**

Add the following secrets:

- `SERPAPI_KEY` - Your SerpAPI key
- `SENDER_EMAIL` - Email address to send from
- `SENDER_PASSWORD` - Email password/app password
- `RECIPIENT_EMAIL` - Email address to receive results
- `SMTP_SERVER` - SMTP server (e.g., smtp.gmail.com)
- `SMTP_PORT` - SMTP port (e.g., 587)
- `SEARCH_QUERY` - Your search query (e.g., "law firm vacation scheme 2025 UK")

### 3. Enable GitHub Actions

Make sure GitHub Actions are enabled in your repository:
**Settings → Actions → General → Allow all actions**

### 4. Configure Workflow Permissions

Go to **Settings → Actions → General → Workflow permissions**
- Select "Read and write permissions"
- Check "Allow GitHub Actions to create and approve pull requests"

### 5. Manual Test Run

Go to **Actions** tab → **Vacation Scheme Search** → **Run workflow**

The workflow will:
1. Install dependencies
2. Run the search
3. Email new results
4. Commit and push `sent_urls.json` back to the repo

### 6. Scheduled Runs

The workflow runs automatically every day at 9 AM UTC. You can modify the schedule in `.github/workflows/vacation_scheme_search.yml`:

```yaml
schedule:
  - cron: '0 9 * * *'  # Change time as needed
```

Cron format: `minute hour day month weekday`
Examples:
- `0 9 * * *` - 9 AM daily
- `0 9,18 * * *` - 9 AM and 6 PM daily
- `0 9 * * 1,3,5` - 9 AM on Mon, Wed, Fri

### 7. Monitor Runs

Check the **Actions** tab to see run history and logs.
