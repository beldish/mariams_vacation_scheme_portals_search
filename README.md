# Mariam's Vacation Scheme Search Agent

An automated AI agent that searches for vacation scheme opportunities around Oxfordshire and Bristol for law students and sends results via email.

## Features

- 🔍 Automated search using SerpAPI
- 📧 Email notifications with formatted results
- ⏰ Scheduled to run every Monday at 7:00 AM London time
- 🐧 Designed for Linux systems
- 🔒 Secure configuration management

## Requirements

- Python 3.7 or higher
- Linux operating system
- SerpAPI account and API key (https://serpapi.com)
- Gmail account with App Password enabled

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/beldish/mariams_vacation_scheme_portals_search.git
cd mariams_vacation_scheme_portals_search
```

### 2. Install Python dependencies

```bash
pip3 install -r requirements.txt
```

### 3. Configure the application

Copy the example configuration file and edit it with your credentials:

```bash
cp config.ini.example config.ini
nano config.ini
```

Edit the following values in `config.ini`:

- `api_key` - Your SerpAPI key from https://serpapi.com
- `sender_password` - Your Gmail App Password (see below for setup)

#### Setting up Gmail App Password

1. Go to your Google Account settings
2. Navigate to Security
3. Enable 2-Step Verification if not already enabled
4. Go to "App passwords" under "Signing in to Google"
5. Generate a new app password for "Mail"
6. Copy the generated password to `config.ini`

## Usage

### Run Once (Manual Search)

To run a single search immediately:

```bash
python3 search_agent.py
```

### Run with Scheduler

To start the scheduler that will run every Monday at 7 AM London time:

```bash
python3 scheduler.py
```

The scheduler will keep running in the foreground. Press `Ctrl+C` to stop it.

### Run as a System Service (Recommended for Production)

To run the agent as a systemd service that starts automatically:

1. Edit the service file with your paths:

```bash
nano vacation-scheme-search.service
```

Update:
- `User=YOUR_USERNAME` - Your Linux username
- `WorkingDirectory=/path/to/mariams_vacation_scheme_portals_search` - Full path to this directory
- `ExecStart=/usr/bin/python3 /path/to/mariams_vacation_scheme_portals_search/scheduler.py` - Full path to scheduler.py

2. Copy the service file to systemd:

```bash
sudo cp vacation-scheme-search.service /etc/systemd/system/
```

3. Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable vacation-scheme-search.service
sudo systemctl start vacation-scheme-search.service
```

4. Check the service status:

```bash
sudo systemctl status vacation-scheme-search.service
```

5. View logs:

```bash
sudo journalctl -u vacation-scheme-search.service -f
```

## Configuration

The `config.ini` file contains all configuration options:

### [serpapi]
- `api_key` - Your SerpAPI API key

### [email]
- `sender_email` - Email address to send from (mishabeldi@gmail.com)
- `sender_password` - Gmail App Password
- `recipient_email` - Email address to send to (mishabeldi@yahoo.com)
- `smtp_server` - SMTP server (smtp.gmail.com)
- `smtp_port` - SMTP port (587)

### [search]
- `query` - Search query for vacation schemes
- `schedule_time` - Time to run daily (format: HH:MM)
- `schedule_day` - Day of week to run (monday)
- `timezone` - Timezone for scheduling (Europe/London)

## Search Query

The default search query is:
```
Vacation Scheme portals around Oxfordshire and Bristol for a third year law student from York
```

You can modify this in the `config.ini` file under the `[search]` section.

## Email Format

The agent sends HTML-formatted emails containing:
- Search query used
- Date and time of search
- List of results with titles, links, and descriptions
- Formatted for easy reading

## Troubleshooting

### Email not sending
- Verify Gmail App Password is correct
- Ensure 2-Step Verification is enabled on Gmail
- Check that "Less secure app access" is not blocking the connection

### SerpAPI errors
- Verify your API key is valid
- Check your SerpAPI account has remaining credits
- Visit https://serpapi.com/dashboard to check usage

### Scheduler not running
- Check the system time and timezone are correct
- Verify the service is running: `sudo systemctl status vacation-scheme-search.service`
- Check logs: `sudo journalctl -u vacation-scheme-search.service`

## Security Notes

- ⚠️ **Never commit `config.ini` to version control** - it contains sensitive credentials
- The `.gitignore` file is configured to exclude `config.ini`
- Use `config.ini.example` as a template only

## License

This project is provided as-is for personal use.

## Support

For issues or questions, please open an issue on GitHub.
