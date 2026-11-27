
from flask import Flask, render_template, request
import heapq

app = Flask(__name__)

GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)


def get_neighbors(state):
    neighbors = []
    zero = state.index(0)
    row, col = divmod(zero, 3)

    moves = [
        (-1, 0), (1, 0), (0, -1), (0, 1)
    ]

    for dr, dc in moves:
        new_row = row + dr
        new_col = col + dc

        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_pos = new_row * 3 + new_col
            new_state = list(state)

            new_state[zero], new_state[new_pos] = (
                new_state[new_pos], new_state[zero]
            )

            neighbors.append(tuple(new_state))

    return neighbors


def misplaced_tiles(state):
    return sum(
        1 for i in range(9)
        if state[i] != 0 and state[i] != GOAL[i]
    )


def manhattan_distance(state):
    distance = 0

    for i, value in enumerate(state):
        if value != 0:
            current_row, current_col = divmod(i, 3)
            goal_row, goal_col = divmod(value - 1, 3)

            distance += (
                abs(current_row - goal_row)
                + abs(current_col - goal_col)
            )

    return distance


def is_solvable(state):
    numbers = [x for x in state if x != 0]

    inversions = 0
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] > numbers[j]:
                inversions += 1

    return inversions % 2 == 0


def a_star(start, heuristic):
    if not is_solvable(start):
        return None

    if heuristic == "manhattan":
        h = manhattan_distance
    else:
        h = misplaced_tiles

    priority_queue = []
    heapq.heappush(priority_queue, (h(start), 0, start))

    visited = set()
    parent = {start: None}
    cost = {start: 0}

    while priority_queue:
        _, g, current = heapq.heappop(priority_queue)

        if current in visited:
            continue

        visited.add(current)

        if current == GOAL:
            path = []
            state = current

            while state is not None:
                path.append(state)
                state = parent[state]

            return path[::-1]

        for neighbor in get_neighbors(current):
            new_cost = g + 1

            if neighbor not in cost or new_cost < cost[neighbor]:
                cost[neighbor] = new_cost
                parent[neighbor] = current

                priority = new_cost + h(neighbor)

                heapq.heappush(
                    priority_queue,
                    (priority, new_cost, neighbor)
                )

    return None


@app.route("/", methods=["GET", "POST"])
def index():
    solution = None
    error = None
    heuristic = "manhattan"
    initial_state = [1, 2, 3, 4, 5, 6, 7, 0, 8]

    if request.method == "POST":
        try:
            initial_state = [
                int(request.form[f"cell{i}"])
                for i in range(9)
            ]

            heuristic = request.form.get(
                "heuristic", "manhattan"
            )

            if sorted(initial_state) != list(range(9)):
                raise ValueError(
                    "Enter every number from 0 to 8 exactly once."
                )

            path = a_star(tuple(initial_state), heuristic)

            if path is None:
                error = "This puzzle is not solvable."
            else:
                solution = [
                    [list(state[i:i + 3]) for i in range(0, 9, 3)]
                    for state in path
                ]

        except ValueError as e:
            error = str(e)

    return render_template(
        "index.html",
        solution=solution,
        error=error,
        heuristic=heuristic,
        initial_state=initial_state
    )


if __name__ == "__main__":
    app.run(debug=True)
