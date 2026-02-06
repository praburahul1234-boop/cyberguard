from flask import Flask, render_template, request

app = Flask(__name__)

def analyze_risk(message, link):
    risk = 0
    message = message.lower()
    link = link.lower()

    # Message urgent words
    urgent_words = ["urgent", "blocked", "verify", "click now", "win", "free"]
    for word in urgent_words:
        if word in message:
            risk += 30

    # Website checks
    if not link.startswith("https://"):
        risk += 30
    if "@" in link:
        risk += 40
    if link.count(".") > 3:
        risk += 20
    if len(link) > 60:
        risk += 20

    bad_words = ["login", "verify", "secure", "bank", "update", "free", "offer"]
    for word in bad_words:
        if word in link:
            risk += 20

    # Final result
    if risk <= 20:
        return "🟢 GREEN – SAFE", "green"
    elif risk <= 60:
        return "🟡 YELLOW – SUSPICIOUS", "orange"
    else:
        return "🔴 RED – DANGEROUS", "red"

@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    color = ""

    if request.method == "POST":
        message = request.form["message"]
        link = request.form["link"]
        result, color = analyze_risk(message, link)

    return render_template("index.html", result=result, color=color)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0, port=10000)
