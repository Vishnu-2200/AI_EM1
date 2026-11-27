
from flask import Flask, render_template, request

app = Flask(__name__)


def plan_blocks(initial, goal):
    current = initial[:]
    steps = ["Initial arrangement: " + " ".join(current)]

    for position, block in enumerate(goal):
        if position < len(current) and current[position] == block:
            continue

        if block in current:
            current.remove(block)

        current.insert(position, block)
        steps.append("Move " + block + " into position " + str(position + 1)
                     + ": " + " ".join(current))

    return steps


@app.route("/", methods=["GET", "POST"])
def index():
    steps = None
    error = None

    if request.method == "POST":
        initial_text = request.form.get("initial", "").upper().strip()
        goal_text = request.form.get("goal", "").upper().strip()

        initial = initial_text.split()
        goal = goal_text.split()

        if not initial or not goal:
            error = "Please enter both arrangements."
        elif len(initial) != len(goal) or set(initial) != set(goal):
            error = "Both arrangements must contain the same blocks exactly once."
        elif len(set(initial)) != len(initial):
            error = "Do not enter duplicate blocks."
        else:
            steps = plan_blocks(initial, goal)

    return render_template("index.html", steps=steps, error=error)


if __name__ == "__main__":
    app.run(debug=True)
