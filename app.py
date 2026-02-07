from flask import Flask, request, jsonify
from datetime import datetime
import csv

def load_messages():
    messages = []
    try:
        with open("messages.csv", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                messages.append(row)
    except FileNotFoundError:
        pass
    return messages

app = Flask(__name__)

@app.route("/")
def home():
    return "Yui server is alive!"

@app.route("/submit", methods=["POST"])
def submit():
    # WebflowのWebhookは form じゃなく json で来ることが多いので両対応にする
    data = request.get_json(silent=True) or {}
    # 念のためフォーム形式でも受けられるように
    name = request.form.get("name") or data.get("name") or ""
    message = request.form.get("message") or data.get("message") or data.get("email") or ""
    print("---- received ----")
    print("name:", name)
    print("message:", message)
    with open("messages.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().isoformat(),
            name,
            message
        ])
    return jsonify({
        "ok": True,
        "name": name,
        "message": message,
        "server_time": datetime.now().isoformat()
})
@app.route("/admin")
def admin():
    messages = load_messages()

    html = "<h1>Messages</h1><ul>"
    for time, name, message in messages:
        html += f"<li>{time} / {name} : {message}</li>"
    html += "</ul>"

    return html
