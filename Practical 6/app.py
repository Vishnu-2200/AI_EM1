
from flask import Flask, render_template

app = Flask(__name__)

GRAPH = {
    "A": ["B", "C"],
    "B": ["A", "C", "D"],
    "C": ["A", "B", "D"],
    "D": ["B", "C"]
}

COLORS = ["Red", "Green", "Blue"]


def is_valid(node, color, assignment):
    for neighbor in GRAPH[node]:
        if assignment.get(neighbor) == color:
            return False
    return True


def backtracking(assignment):
    if len(assignment) == len(GRAPH):
        return assignment

    node = next(n for n in GRAPH if n not in assignment)

    for color in COLORS:
        if is_valid(node, color, assignment):
            assignment[node] = color

            result = backtracking(assignment)
            if result:
                return result

            del assignment[node]

    return None


@app.route("/")
def index():
    solution = backtracking({})
    return render_template("index.html", solution=solution)


if __name__ == "__main__":
    app.run(debug=True)
