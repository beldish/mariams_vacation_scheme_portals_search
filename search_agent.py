#!/usr/bin/env python3
"""
Vacation Scheme Search Agent

This script searches for vacation scheme opportunities using SerpAPI
and sends the results via email. It's designed to run on a schedule.
"""

import configparser
import smtplib
import sys
import html
import json
import os
import subprocess
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from serpapi import GoogleSearch


class VacationSchemeSearchAgent:
    """Agent for searching vacation scheme opportunities and sending results via email."""
    
    def __init__(self, config_file='config.ini', sent_urls_file='sent_urls.json'):
        """Initialize the agent with configuration."""
        self.config = configparser.ConfigParser()
        self.use_env_vars = not os.path.exists(config_file)
        
        if self.use_env_vars:
            print(f"[{datetime.now()}] Config file not found, using environment variables")
            self._load_config_from_env()
        else:
            self.config.read(config_file)
        
        self.sent_urls_file = sent_urls_file
        self.sent_urls = self._load_sent_urls()
        
        # Validate required configuration
        self._validate_config()
    
    def _load_config_from_env(self):
        """Load configuration from environment variables."""
        # Create config sections
        self.config.add_section('serpapi')
        self.config.add_section('email')
        self.config.add_section('search')
        
        # Load from environment variables
        self.config.set('serpapi', 'api_key', os.getenv('SERPAPI_KEY', ''))
        self.config.set('email', 'sender_email', os.getenv('SENDER_EMAIL', ''))
        self.config.set('email', 'sender_password', os.getenv('SENDER_PASSWORD', ''))
        self.config.set('email', 'recipient_email', os.getenv('RECIPIENT_EMAIL', ''))
        self.config.set('email', 'smtp_server', os.getenv('SMTP_SERVER', ''))
        self.config.set('email', 'smtp_port', os.getenv('SMTP_PORT', '587'))
        self.config.set('search', 'query', os.getenv('SEARCH_QUERY', ''))
    
    def _load_sent_urls(self):
        """Load previously sent URLs from file."""
        if os.path.exists(self.sent_urls_file):
            try:
                with open(self.sent_urls_file, 'r') as f:
                    return set(json.load(f))
            except (json.JSONDecodeError, IOError):
                return set()
        return set()
    
    def _save_sent_urls(self):
        """Save sent URLs to file."""
        try:
            with open(self.sent_urls_file, 'w') as f:
                json.dump(list(self.sent_urls), f, indent=2)
        except IOError as e:
            print(f"[{datetime.now()}] Warning: Could not save sent URLs: {e}", file=sys.stderr)
    
    def _commit_sent_urls(self):
        """Commit and push sent URLs file to git repository."""
        try:
            # Check if there are changes to commit
            result = subprocess.run(
                ['git', 'diff', '--quiet', self.sent_urls_file],
                cwd=os.path.dirname(os.path.abspath(__file__)) or '.',
                capture_output=True
            )
            
            # If exit code is 1, there are changes
            if result.returncode == 1:
                print(f"[{datetime.now()}] Committing {self.sent_urls_file} to git...")
                
                # Add the file
                subprocess.run(
                    ['git', 'add', self.sent_urls_file],
                    cwd=os.path.dirname(os.path.abspath(__file__)) or '.',
                    check=True
                )
                
                # Commit the file
                commit_msg = f"Update sent URLs - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                subprocess.run(
                    ['git', 'commit', '-m', commit_msg],
                    cwd=os.path.dirname(os.path.abspath(__file__)) or '.',
                    check=True
                )
                
                # Push to remote
                subprocess.run(
                    ['git', 'push'],
                    cwd=os.path.dirname(os.path.abspath(__file__)) or '.',
                    check=True
                )
                
                print(f"[{datetime.now()}] Successfully pushed {self.sent_urls_file} to repository")
            else:
                print(f"[{datetime.now()}] No changes to commit for {self.sent_urls_file}")
                
        except subprocess.CalledProcessError as e:
            print(f"[{datetime.now()}] Warning: Could not commit to git: {e}", file=sys.stderr)
        except Exception as e:
            print(f"[{datetime.now()}] Warning: Git operation failed: {e}", file=sys.stderr)
    
    def _validate_config(self):
        """Validate that all required configuration is present."""
        required_sections = ['serpapi', 'email', 'search']
        for section in required_sections:
            if not self.config.has_section(section):
                raise ValueError(f"Missing required configuration section: {section}")
        
        # Check for required keys
        if not self.config.get('serpapi', 'api_key'):
            raise ValueError("SerpAPI key not configured")
        if not self.config.get('email', 'sender_email'):
            raise ValueError("Sender email not configured")
        if not self.config.get('search', 'query'):
            raise ValueError("Search query not configured")
    
    def search_vacation_schemes(self):
        """
        Search for vacation schemes using SerpAPI.
        
        Returns:
            dict: Search results from SerpAPI
        """
        print(f"[{datetime.now()}] Starting search...")
        
        params = {
            "q": self.config.get('search', 'query'),
            "location": "United Kingdom",
            "api_key": self.config.get('serpapi', 'api_key'),
            "num": 10  # Number of results
        }
        
        search = GoogleSearch(params)
        results = search.get_dict()
        
        print(f"[{datetime.now()}] Search completed successfully")
        return results
    
    def format_results(self, results):
        """
        Format search results into a readable email body.
        
        Args:
            results (dict): Raw results from SerpAPI
            
        Returns:
            str: Formatted HTML email body
        """
        html_body = """
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                h1 {{ color: #2c3e50; }}
                h2 {{ color: #34495e; margin-top: 20px; }}
                .result {{ 
                    border: 1px solid #ddd; 
                    padding: 15px; 
                    margin: 10px 0; 
                    border-radius: 5px;
                    background-color: #f9f9f9;
                }}
                .title {{ font-weight: bold; color: #2980b9; font-size: 16px; }}
                .link {{ color: #27ae60; word-break: break-all; }}
                .snippet {{ color: #555; margin-top: 5px; }}
                .footer {{ margin-top: 30px; color: #7f8c8d; font-size: 12px; }}
            </style>
        </head>
        <body>
            <h1>Vacation Scheme Search Results</h1>
            <p><strong>Search Query:</strong> {query}</p>
            <p><strong>Search Date:</strong> {date}</p>
            <hr>
        """.format(
            query=self.config.get('search', 'query'),
            date=datetime.now().strftime('%B %d, %Y at %H:%M %Z')
        )
        
        # Add organic results (filter out already sent URLs)
        if 'organic_results' in results and results['organic_results']:
            new_results = [r for r in results['organic_results'] if r.get('link') not in self.sent_urls]
            
            if new_results:
                html_body += "<h2>New Search Results</h2>"
                for idx, result in enumerate(new_results, 1):
                    title = html.escape(result.get('title', 'No title'))
                    link = html.escape(result.get('link', '#'))
                    snippet = html.escape(result.get('snippet', 'No description available'))
                    
                    html_body += f"""
                    <div class="result">
                        <div class="title">{idx}. {title}</div>
                        <div class="link"><a href="{link}">{link}</a></div>
                        <div class="snippet">{snippet}</div>
                    </div>
                    """
                    
                    # Track this URL as sent
                    self.sent_urls.add(result.get('link'))
            else:
                html_body += "<p>No new results found. All results have been sent previously.</p>"
        else:
            html_body += "<p>No results found for this search query.</p>"
        
        # Add footer
        html_body += """
            <hr>
            <div class="footer">
                <p>This is an automated email from the Vacation Scheme Search Agent.</p>
                <p>Search powered by SerpAPI</p>
            </div>
        </body>
        </html>
        """
        
        return html_body
    
    def send_email(self, subject, html_body):
        """
        Send results via email.
        
        Args:
            subject (str): Email subject
            html_body (str): HTML email body
        """
        sender_email = self.config.get('email', 'sender_email')
        sender_password = self.config.get('email', 'sender_password')
        recipient_email = self.config.get('email', 'recipient_email')
        smtp_server = self.config.get('email', 'smtp_server')
        smtp_port = self.config.getint('email', 'smtp_port')
        
        print(f"[{datetime.now()}] Preparing email...")
        
        # Create message
        message = MIMEMultipart('alternative')
        message['Subject'] = subject
        message['From'] = sender_email
        message['To'] = recipient_email
        
        # Attach HTML body
        html_part = MIMEText(html_body, 'html')
        message.attach(html_part)
        
        # Send email
        try:
            print(f"[{datetime.now()}] Connecting to SMTP server...")
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(message)
            print(f"[{datetime.now()}] Email sent successfully to {recipient_email}")
        except Exception as e:
            print(f"[{datetime.now()}] Error sending email: {str(e)}", file=sys.stderr)
            raise
    
    def run(self):
        """Execute the search and email workflow."""
        try:
            print(f"[{datetime.now()}] Starting Vacation Scheme Search Agent...")
            
            # Search for vacation schemes
            results = self.search_vacation_schemes()
            
            # Format results
            html_body = self.format_results(results)
            
            # Send email
            subject = f"Vacation Scheme Search Results - {datetime.now().strftime('%B %d, %Y')}"
            self.send_email(subject, html_body)
            
            # Save the updated list of sent URLs
            self._save_sent_urls()
            print(f"[{datetime.now()}] Saved {len(self.sent_urls)} sent URLs")
            
            # Commit and push to git repository
            self._commit_sent_urls()
            
            print(f"[{datetime.now()}] Agent completed successfully")
            return True
            
        except Exception as e:
            print(f"[{datetime.now()}] Error in agent execution: {str(e)}", file=sys.stderr)
            return False


if __name__ == "__main__":
    agent = VacationSchemeSearchAgent()
    success = agent.run()
    sys.exit(0 if success else 1)
