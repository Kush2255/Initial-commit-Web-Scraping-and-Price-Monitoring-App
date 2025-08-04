# 🛒 Amazon & Flipkart Price Tracker with GUI, Alerts, and Scheduler

A powerful Python-based price monitoring app that tracks product prices on **Amazon** and **Flipkart**, sends email alerts for price drops, stores historical data, and features a simple desktop GUI built with **Tkinter**.

---

## ✨ Features

- 🔍 **Track Multiple Products**  
  Monitor product prices from Amazon and Flipkart.

- 🖱️ **Simple GUI**  
  Built with Tkinter for easy user interaction.

- ⏰ **Daily Scheduled Scraping**  
  Automatically runs scraping in the background at set times.

- ✉️ **Email Alerts**  
  Notifies you instantly when a price drops below your specified threshold.

- 🗃️ **SQLite/MySQL Storage**  
  Saves product titles and prices locally or to a MySQL database.

- 📤 **Optional Excel Export**  
  Extendable to support Excel export of price history.

- 🧠 **Robust Error Handling & Logging**

---

## 🖼️ GUI Overview

- Enter Amazon or Flipkart product search URL  
- Set a threshold price (₹)  
- Click **"Start Scraping"**  
- Get feedback: ✅ *Scraping Done* or ✉️ *Email Sent*  
- Scheduler runs daily checks in the background

---

## 📁 Project Highlights

| Component       | Description                                      |
|-----------------|--------------------------------------------------|
| **Frontend**    | Tkinter GUI for user interaction                 |
| **Scraping**    | Selenium-based dynamic scraping engine           |
| **Backend**     | SQLite & MySQL integration                       |
| **Email System**| SMTP-based alerts using Gmail                    |
| **Scheduler**   | Python `schedule` module for timed scraping      |

---

## 🧩 Technologies Used

- Python 3.11+
- Selenium
- BeautifulSoup
- Schedule
- Tkinter (GUI)
- MySQL / SQLite
- SMTP (Email Alerts)

---

## ✅ Requirements

- Python 3.11 or later
- Google Chrome browser installed
- ChromeDriver (compatible with your Chrome version)
- MySQL (optional for DB storage)

### 🔧 Python Libraries
Install dependencies with:
```bash
pip install -r requirements.txt
