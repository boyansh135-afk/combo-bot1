import telebot
import json

# 📁 Load config
with open("config.json") as f:
    config = json.load(f)

bot = telebot.TeleBot(config["token"])
ADMIN_ID = config["user_id"]
GROUP_ID = config["group_id"]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "👋 Combo Bot Activated!\nUse /help to see available commands.")

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, """
🧠 Study Assistant + 📈 Trading Alerts Bot

Available Commands:
/start - Welcome message
/help - Show this help
/alert - Run Daily Stock Alerts Now
""")

@bot.message_handler(commands=['alert'])
def run_alerts(message):
    from daily_alert import run_all_alerts
    run_all_alerts()
    bot.send_message(message.chat.id, "✅ Alerts Executed!")

bot.polling()