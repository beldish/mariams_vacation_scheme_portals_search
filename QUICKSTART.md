# Quick Start Guide

Get the Vacation Scheme Search Agent running in 5 minutes!

## Prerequisites

- Linux system
- Python 3.7+
- SerpAPI account (sign up at https://serpapi.com)
- Gmail account with 2FA enabled

## Setup Steps

### 1. Get Your API Keys

**SerpAPI Key:**
1. Go to https://serpapi.com
2. Sign up for a free account
3. Copy your API key from the dashboard

**Gmail App Password:**
1. Enable 2-Step Verification in your Google Account
2. Go to Security → App passwords
3. Generate new password for "Mail"
4. Save this password (you won't see it again)

### 2. Install Dependencies

```bash
# Run the setup script
chmod +x setup.sh
./setup.sh
```

### 3. Configure the Agent

Edit `config.ini` and replace:
- `YOUR_SERPAPI_KEY_HERE` with your actual SerpAPI key
- `YOUR_GMAIL_APP_PASSWORD_HERE` with your Gmail app password

```bash
nano config.ini
```

### 4. Test the Agent

Run a single search to verify everything works:

```bash
python3 search_agent.py
```

You should receive an email with search results!

### 5. Start the Scheduler

Keep the agent running and it will automatically search every Monday at 7 AM:

```bash
python3 scheduler.py
```

Press `Ctrl+C` to stop.

## Production Deployment

To run 24/7 as a background service:

1. Edit `vacation-scheme-search.service`:
   - Replace `YOUR_USERNAME` with your Linux username
   - Replace `/path/to/mariams_vacation_scheme_portals_search` with full path

2. Install the service:
```bash
sudo cp vacation-scheme-search.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable vacation-scheme-search.service
sudo systemctl start vacation-scheme-search.service
```

3. Check status:
```bash
sudo systemctl status vacation-scheme-search.service
```

## Troubleshooting

**"Authentication failed" when sending email:**
- Make sure you're using an App Password, not your regular Gmail password
- Verify 2FA is enabled on your Google account

**"Invalid API key" from SerpAPI:**
- Check your API key is copied correctly
- Verify your SerpAPI account has available credits

**No email received:**
- Check your spam folder
- Verify recipient email is correct in config.ini

## Next Steps

- See `README.md` for full documentation
- Customize the search query in `config.ini`
- Change the schedule time if needed

## Support

Open an issue on GitHub if you encounter problems!
