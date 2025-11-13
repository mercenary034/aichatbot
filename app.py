from chatbot import CB
from flask import Flask, render_template, request
import threading
import time
import re
from datetime import datetime, timedelta

app = Flask(__name__)

def alarm_thread(alarm_time):
    now = datetime.now()
    seconds_until_alarm = (alarm_time - now).total_seconds()
    if seconds_until_alarm > 0:
        time.sleep(seconds_until_alarm)
        print(f"Alarm! It's now {alarm_time.strftime('%H:%M')}")
    else:
        print("Alarm time is in the past, skipping alarm.")

def parse_alarm_time(userText):
    # Support HH:MM and H with optional am/pm
    match = re.search(r'(\d{1,2})(?::(\d{2}))?\s*(am|pm)?', userText, re.IGNORECASE)
    if match:
        hour = int(match.group(1))
        minute = int(match.group(2)) if match.group(2) else 0
        meridiem = match.group(3)

        if meridiem:
            meridiem = meridiem.lower()
            if meridiem == 'pm' and hour != 12:
                hour += 12
            elif meridiem == 'am' and hour == 12:
                hour = 0

        now = datetime.now()
        alarm_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if alarm_time < now:
            alarm_time += timedelta(days=1)
        return alarm_time
    return None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg', '')
    lower_text = userText.lower()

    alarm_keywords = ['set alarm', 'alarm for', 'wake me up at', 'remind me at']
    if any(keyword in lower_text for keyword in alarm_keywords):
        alarm_time = parse_alarm_time(userText)
        if alarm_time:
            threading.Thread(target=alarm_thread, args=(alarm_time,), daemon=True).start()
            return f"Alarm set for {alarm_time.strftime('%H:%M')}"
        else:
            return "Sorry, I couldn't understand the alarm time. Please specify in HH:MM format."

    return str(CB.get_response(userText))

if __name__ == "__main__":
    app.run(debug=True)
