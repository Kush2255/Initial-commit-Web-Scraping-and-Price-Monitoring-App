import tkinter as tk
from tkinter import messagebox
import time
import sqlite3
import mysql.connector
import threading
import schedule
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from webdriver_manager.chrome import ChromeDriverManager

# Email Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_ADDRESS = "sarayukush@gmail.com"
EMAIL_PASSWORD = "irzi lktv rpmk ofrd"
TO_EMAIL = "mayupawar183@gmail.com"

def send_email_alert(product_title, product_price):
    subject = "Price Drop Alert!"
    body = f"Good news!\n\nThe price of '{product_title}' has dropped to ₹{product_price}.\nCheck it on the website!"

    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print(f"✅ Email sent for: {product_title} @ ₹{product_price}")
    except Exception as e:
        print("❌ Email failed:", e)

# Amazon Scraper
def amazon_scraper(url, threshold_price):
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")
    options.add_argument("user-agent=Mozilla/5.0")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(4)
    for _ in range(3):
        driver.execute_script("window.scrollBy(0, 1000)")
        time.sleep(2)

    script = """
        let data = [];
        let items = document.querySelectorAll("div.s-main-slot div[data-component-type='s-search-result']");
        items.forEach(item => {
            let title = item.querySelector("h2 span")?.innerText?.trim() || "No title";
            let price = item.querySelector(".a-price .a-offscreen")?.innerText?.replace(/[₹,]/g, '').trim();
            if(title && price) data.push({title, price});
        });
        return data;
    """
    results = driver.execute_script(script)
    driver.quit()

    conn = sqlite3.connect("amazon_products.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS products(ID INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, price TEXT)")
    for item in results:
        cur.execute("INSERT INTO products(title, price) VALUES (?,?)", (item["title"], item["price"]))
        try:
            if int(item["price"]) <= threshold_price:
                send_email_alert(item["title"], item["price"])
        except:
            pass
    conn.commit()
    conn.close()

    try:
        mysql_conn = mysql.connector.connect(
            host="localhost", user="root", password="iare", database="amazon_products"
        )
        mysql_cur = mysql_conn.cursor()
        mysql_cur.execute("CREATE TABLE IF NOT EXISTS products(id INT AUTO_INCREMENT PRIMARY KEY, title TEXT, price TEXT)")
        sqlite3_conn = sqlite3.connect("amazon_products.db")
        sqlite3_cur = sqlite3_conn.cursor()
        sqlite3_cur.execute("SELECT title, price FROM products")
        for row in sqlite3_cur.fetchall():
            mysql_cur.execute("INSERT INTO products(title, price) VALUES (%s, %s)", row)
        mysql_conn.commit()
    finally:
        try: mysql_conn.close(); sqlite3_conn.close()
        except: pass

# Flipkart Scraper
def flipkart_scraper(url, threshold_price):
    options = Options()
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    try:
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'✕')]"))).click()
    except: pass
    for _ in range(3): driver.execute_script("window.scrollBy(0, 1000)"); time.sleep(1)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()

    titles = soup.find_all("div", class_="KzDlHZ")
    prices = soup.find_all("div", class_=["Nx9bqj", "_4b5DiR"])

    conn = sqlite3.connect("flipkart_products.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS products(ID INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, price TEXT)")

    for i in range(min(len(titles), len(prices))):
        title = titles[i].text.strip()
        price = prices[i].text.strip().replace("₹", "").replace(",", "")
        cur.execute("INSERT INTO products(title, price) VALUES (?, ?)", (title, price))
        try:
            if int(price) <= threshold_price:
                send_email_alert(title, price)
        except:
            pass
    conn.commit()
    conn.close()

    try:
        mysql_conn = mysql.connector.connect(
            host="localhost", user="root", password="iare", database="flipcart_products"
        )
        mysql_cur = mysql_conn.cursor()
        mysql_cur.execute("CREATE TABLE IF NOT EXISTS products(id INT AUTO_INCREMENT PRIMARY KEY, title TEXT, price TEXT)")
        sqlite3_conn = sqlite3.connect("flipkart_products.db")
        sqlite3_cur = sqlite3_conn.cursor()
        sqlite3_cur.execute("SELECT title, price FROM products")
        for row in sqlite3_cur.fetchall():
            mysql_cur.execute("INSERT INTO products(title, price) VALUES (%s, %s)", row)
        mysql_conn.commit()
    finally:
        try: mysql_conn.close(); sqlite3_conn.close()
        except: pass

# Scheduler
def run_scheduler():
    threshold = 80000
    schedule.every().day.at("01:00").do(lambda: amazon_scraper("https://www.amazon.in/s?k=laptop", threshold))
    schedule.every().day.at("01:00").do(lambda: flipkart_scraper("https://www.flipkart.com/search?q=laptop", threshold))
    while True:
        schedule.run_pending()
        time.sleep(1)

# GUI Start Function
def start_scraper():
    url = url_entry.get().strip()
    threshold_str = threshold_entry.get().strip()

    if not url or not threshold_str:
        messagebox.showerror("Missing Info", "Please enter both URL and threshold price.")
        return

    try:
        threshold_price = int(threshold_str)
    except ValueError:
        messagebox.showerror("Invalid", "Threshold price must be a number.")
        return

    message_label.config(text="🔄 Scraping in progress...", fg="blue")
    root.update()

    try:
        if "amazon" in url:
            amazon_scraper(url, threshold_price)
            messagebox.showinfo("✅ Success", "Amazon scraping completed successfully!")
            message_label.config(text="✅ Amazon scraping done!", fg="green")
        elif "flipkart" in url:
            flipkart_scraper(url, threshold_price)
            messagebox.showinfo("✅ Success", "Flipkart scraping completed successfully!")
            message_label.config(text="✅ Flipkart scraping done!", fg="green")
        else:
            messagebox.showerror("❌ Failed", "Only Amazon or Flipkart URLs are supported.")
            message_label.config(text="❌ Scraping failed", fg="red")
    except Exception as e:
        messagebox.showerror("Error", f"Scraping failed.\n{e}")
        message_label.config(text="❌ Error occurred", fg="red")

# GUI Setup
root = tk.Tk()
root.title("Product Price Scraper")
root.geometry("500x260")

tk.Label(root, text="Enter Amazon or Flipkart Search URL:", font=("Arial", 11)).pack(pady=10)
url_entry = tk.Entry(root, width=65)
url_entry.pack()

tk.Label(root, text="Enter Threshold Price (₹):", font=("Arial", 11)).pack(pady=5)
threshold_entry = tk.Entry(root, width=20)
threshold_entry.pack()

tk.Button(root, text="Start Scraping", font=("Arial", 10), command=start_scraper).pack(pady=10)
message_label = tk.Label(root, text="", font=("Arial", 10))
message_label.pack()

# Start Scheduler Thread
scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

# Launch GUI
root.mainloop()
