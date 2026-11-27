
from flask import Flask, render_template, request

app = Flask(__name__)


def diagnose(answers):
    if answers["internet"] == "yes":
        return "Your internet connection is working properly."

    if answers["wifi"] == "no":
        return "Turn on Wi-Fi and connect to an available network."

    if answers["other_device"] == "yes":
        return "The problem may be with your device. Restart it and reconnect."

    if answers["router"] == "no":
        return "Check your router power and cables."

    return "Restart your router. If the problem continues, contact your ISP."


@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        answers = {
            "internet": request.form.get("internet"),
            "wifi": request.form.get("wifi"),
            "other_device": request.form.get("other_device"),
            "router": request.form.get("router")
        }

        result = diagnose(answers)

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
