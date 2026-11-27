
from flask import Flask, render_template, request
from sklearn.tree import DecisionTreeClassifier

app = Flask(__name__)

X = [
    [1, 40, 30],
    [2, 50, 35],
    [3, 55, 40],
    [4, 60, 45],
    [5, 70, 55],
    [6, 75, 65],
    [7, 80, 70],
    [8, 85, 80],
    [9, 90, 85],
    [10, 95, 90],
    [2, 45, 25],
    [5, 65, 50],
    [7, 75, 60],
    [8, 90, 75]
]

y = [
    0, 0, 0, 0, 0, 1, 1,
    1, 1, 1, 0, 0, 1, 1
]

model = DecisionTreeClassifier(random_state=42)
model.fit(X, y)


@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    error = None

    if request.method == "POST":
        try:
            hours = float(request.form["study_hours"])
            attendance = float(request.form["attendance"])
            marks = float(request.form["previous_marks"])

            if not 0 <= hours <= 24:
                raise ValueError("Study hours must be between 0 and 24.")

            if not 0 <= attendance <= 100 or not 0 <= marks <= 100:
                raise ValueError("Attendance and marks must be between 0 and 100.")

            result = model.predict([[hours, attendance, marks]])[0]

            prediction = (
                "Good Performance"
                if result == 1
                else "Needs Improvement"
            )

        except ValueError as e:
            error = str(e)

    return render_template(
        "index.html",
        prediction=prediction,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)
