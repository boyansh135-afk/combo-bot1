import telebot
import json
import requests
import gspread
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from utils.inside_breakout import check_inside_breakouts
from utils.fetch_delivery_spike import fetch_delivery_spike
from utils.insider_bulk_deals import check_insider_bulk_deals
from utils.chartink_fetcher import fetch_chartink_data

# Load config
with open("config.json") as f:
    config = json.load(f)

bot = telebot.TeleBot(config["token"])
GROUP_ID = config["group_id"]

# Google Sheet Setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_url(config["sheet_url"]).worksheet(config["sheet_name"].strip())
data = sheet.get_all_values()
stocks = [row[0] for row in data[1:] if row and row[0] != ""]

# Basic breakout checker
def check_breakouts():
    msgs = []
    for symbol in stocks:
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}.NS?range=5d&interval=1d"
            res = requests.get(url)
            result = res.json()["chart"]["result"][0]
            close = result["indicators"]["quote"][0]["close"]
            if len(close) >= 2 and close[-1] > close[-2]:
                msgs.append(f"💥 {symbol} breakout: ₹{close[-1]:.2f}")
        except Exception as e:
            print(f"❌ {symbol}: {e}")
    return msgs

# Run all alerts
def run_all_alerts():
    all_msgs = []

    breakout = check_breakouts()
    if breakout:
        all_msgs.append("📈 Daily Breakouts:\n" + "\n".join(breakout))

    inside = check_inside_breakouts(stocks)
    if inside:
        all_msgs.append("📍 Inside Candle:\n" + "\n".join(inside))

    delivery = fetch_delivery_spike()
    if delivery:
        all_msgs.append("🚚 Delivery Spike:\n" + "\n".join(delivery))

    insider = check_insider_bulk_deals()
    if insider:
        all_msgs.append("📦 Insider/Bulk Deals:\n" + "\n".join(insider))

    chartink = fetch_chartink_data()
    if chartink:
        all_msgs.append("📊 Chartink Picks:\n" + "\n".join(chartink))

    full_msg = "\n\n".join(all_msgs) if all_msgs else "⚠️ No alerts today."
    bot.send_message(GROUP_ID, full_msg)