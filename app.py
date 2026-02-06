from flask import Flask, request, jsonify

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
    return jsonify({"ok": True, "name": name, "message": message})
