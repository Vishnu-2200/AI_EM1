
from flask import Flask, render_template, request

app = Flask(__name__)

ROWS = 4
COLS = 4
GOAL = (3, 3)
OBSTACLES = [(1, 1)]
ACTIONS = {
    "↑": (-1, 0),
    "↓": (1, 0),
    "←": (0, -1),
    "→": (0, 1)
}


def move(state, action):
    dr, dc = ACTIONS[action]
    r, c = state
    nr, nc = r + dr, c + dc

    if not (0 <= nr < ROWS and 0 <= nc < COLS):
        return state

    if (nr, nc) in OBSTACLES:
        return state

    return (nr, nc)


def value_iteration(gamma=0.9, theta=0.001):
    states = [
        (r, c)
        for r in range(ROWS)
        for c in range(COLS)
        if (r, c) not in OBSTACLES
    ]

    values = {state: 0.0 for state in states}

    while True:
        delta = 0

        for state in states:
            if state == GOAL:
                continue

            old_value = values[state]
            action_values = []

            for action in ACTIONS:
                next_state = move(state, action)

                if next_state == GOAL:
                    reward = 10
                else:
                    reward = -1

                action_values.append(
                    reward + gamma * values[next_state]
                )

            values[state] = max(action_values)
            delta = max(delta, abs(old_value - values[state]))

        if delta < theta:
            break

    policy = {}

    for state in states:
        if state == GOAL:
            policy[state] = "G"
            continue

        best_action = None
        best_value = float("-inf")

        for action in ACTIONS:
            next_state = move(state, action)
            reward = 10 if next_state == GOAL else -1
            value = reward + gamma * values[next_state]

            if value > best_value:
                best_value = value
                best_action = action

        policy[state] = best_action

    return values, policy


@app.route("/", methods=["GET", "POST"])
def index():
    values, policy = value_iteration()
    return render_template(
        "index.html",
        values=values,
        policy=policy,
        rows=ROWS,
        cols=COLS,
        obstacles=OBSTACLES,
        goal=GOAL
    )


if __name__ == "__main__":
    app.run(debug=True)
