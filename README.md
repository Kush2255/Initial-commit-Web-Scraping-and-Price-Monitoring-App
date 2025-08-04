🛒 Amazon & Flipkart Price Tracker with GUI, Alerts, and Scheduler
A powerful Python-based price monitoring app that tracks product prices on Amazon and Flipkart, sends email alerts for price drops, stores historical data, and features a simple desktop GUI built with Tkinter.

✨ Key Features
🔍 Track Multiple Products
Monitor prices from Amazon and Flipkart simultaneously.

⏰ Daily Scheduled Scraping
Automatically check prices at set intervals using the built-in scheduler.

✉️ Email Notifications
Get instant alerts when prices fall below your desired threshold.

📊 Data Storage & Export
Store price history in MySQL or SQLite, with optional Excel export.

🖥️ GUI Interface
Add product URLs, set price limits, and run the tracker with just a click.

⚙️ Designed for Windows (Python 3.11+)

🖼️ GUI Overview
The GUI allows you to:

🔗 Enter Amazon or Flipkart product URLs

💸 Set target price thresholds

▶️ Start scraping manually

✅ Get feedback: "Scraping Done" or "Email Sent"

📅 Schedule background scraping jobs

📁 Project Highlights
Component	Description
Frontend	Tkinter GUI for ease of use
Backend	Selenium-based web scraper
Database	MySQL / SQLite integration for storing data
Alerts	Email notifications via SMTP
Scheduler	Auto-run with schedule module or CRON

✅ Requirements
Python 3.11+

Google Chrome browser

MySQL or SQLite

Required Python packages (auto-installed via pip install -r requirements.txt)
