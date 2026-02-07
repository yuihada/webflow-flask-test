from flask import Flask, request, jsonify
from datetime import datetime
import csv
import os

app = Flask(__name__)

# ✅ 保存先を「このapp.pyと同じフォルダ」に固定
DATA_FILE = os.path.join(app.root_path, "messages.csv")


def load_messages():
    messages = []
    try:
        with open(DATA_FILE, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                # 行が壊れてても落ちないように保険
                if len(row) >= 3:
                    messages.append(row[:3])
    except FileNotFoundError:
        pass
    return messages


@app.route("/")
def home():
    return "Yui server is alive!"


@app.route("/submit", methods=["POST"])
def submit():
    print("RAW JSON:", request.get_json(silent=True))
    print("FORM:", request.form)
    
    data = request.get_json(silent=True) or {}

    name = request.form.get("name") or data.get("name") or ""
    message = request.form.get("message") or data.get("message") or data.get("email") or ""

    print("---- received ----")
    print("name:", name)
    print("message:", message)
    print("writing to:", DATA_FILE)

    with open(DATA_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().isoformat(), name, message])

    return jsonify({
        "ok": True,
        "name": name,
        "message": message,
        "server_time": datetime.now().isoformat()
    })

@app.route("/admin")
def admin():
    messages = load_messages()

    html = "<h1>Messages</h1>"
    html += f"<p>Total: {len(messages)}</p>"
    html += "<ul>"

    for time, name, message in messages:
        html += f"<li>{time} / {name} : {message}</li>"

    html += "</ul>"

    if len(messages) == 0:
        html += "<p>(まだ0件！フォーム送信すると増えるよ)</p>"

    return html

# ✅ 追加：いまの状態を目視できるデバッグページ
@app.route("/debug")
def debug():
    exists = os.path.exists(DATA_FILE)
    size = os.path.getsize(DATA_FILE) if exists else 0
    messages = load_messages()

    return jsonify({
        "data_file": DATA_FILE,
        "exists": exists,
        "size_bytes": size,
        "count": len(messages),
        "latest": messages[-1] if messages else None
    })
    
