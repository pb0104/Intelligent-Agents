

from collections import deque
import heapq
from itertools import count


# Defining initial state
initial_state = {
    "At": {("b1", "returned_cart"), ("b2", "returned_cart"), ("b3", "s1")},
    "Held": set(),
    "ShelfAvailable": {"s1", "s2"},
    "Request": {("b3", "u1")},
    "Delivered": set(),
    "RobotEmpty": True,
}

# Defining goal state
goal_state = {
    "At": {("b1", "s1"), ("b2", "s2")},
    "Delivered": {("b3", "u1")},
}



# Defining Actions
def pick(state, book, location):
    """Pick a book from a location"""
    if ("RobotEmpty" in state and state["RobotEmpty"] and
        (book, location) in state.get("At", set())):
        new_state = {
            key: set(val) if isinstance(val, set) else val
            for key, val in state.items()
        }
        new_state["Held"].add(book)
        new_state["At"].remove((book, location))
        new_state["RobotEmpty"] = False
        return new_state
    return None


def place_on_shelf(state, book, shelf):
    """Place a held book on a shelf"""
    if book in state["Held"] and shelf in state["ShelfAvailable"]:
        new_state = {key: set(val) if isinstance(val, set) else val for key, val in state.items()}
        new_state["Held"].remove(book)
        new_state["At"].add((book, shelf))
        new_state["RobotEmpty"] = True
        # Remove shelf from available if we assume 1 book per shelf
        new_state["ShelfAvailable"].remove(shelf)
        return new_state
    return None


def fetch_for_user(state, book, user):
    """Fetch a book from shelf for user"""
    if ("RobotEmpty" in state and state["RobotEmpty"] and
        (book, "s1") in state.get("At", set()) and
        (book, user) in state.get("Request", set()) or (book, user) in state.get("Request", set())):
        new_state = {key: set(val) if isinstance(val, set) else val for key, val in state.items()}
        if (book, "s1") in new_state["At"]:
            new_state["At"].remove((book, "s1"))
        new_state["Held"].add(book)
        new_state["RobotEmpty"] = False
        return new_state
    return None


def deliver(state, book, user):
    """Deliver a held book to a user"""
    if book in state["Held"] and (book, user) in state.get("Request", set()):
        new_state = {key: set(val) if isinstance(val, set) else val for key, val in state.items()}
        new_state["Held"].remove(book)
        new_state["Delivered"].add((book, user))
        new_state["Request"].remove((book, user))
        new_state["RobotEmpty"] = True
        return new_state
    return None

# Helper functions
def goal_satisfied(state, goal):
    """Check if the goal state is satisfied"""
    for key in goal:
        if not goal[key].issubset(state.get(key, set())):
            return False
    return True


def get_possible_actions(state):
    """Return all applicable actions from the current state"""
    actions = []

    # Pick books from cart or shelves
    for (book, loc) in state.get("At", set()):
        if state.get("RobotEmpty", False):
            actions.append(("pick", book, loc))

    # Place held books on shelves
    for book in state.get("Held", set()):
        for shelf in state.get("ShelfAvailable", set()):
            actions.append(("place_on_shelf", book, shelf))

    # Fetch for user (if requested)
    for (book, user) in state.get("Request", set()):
        if state.get("RobotEmpty", False) and (book, "s1") in state.get("At", set()):
            actions.append(("fetch_for_user", book, user))

    # Deliver books to user
    for book in state.get("Held", set()):
        for (b, user) in state.get("Request", set()):
            if book == b:
                actions.append(("deliver", book, user))

    return actions


def apply_action(state, action):
    """Apply an action and return the new state"""
    act, book, obj = action
    if act == "pick":
        return pick(state, book, obj)
    elif act == "place_on_shelf":
        return place_on_shelf(state, book, obj)
    elif act == "fetch_for_user":
        return fetch_for_user(state, book, obj)
    elif act == "deliver":
        return deliver(state, book, obj)
    return None



# BFS Planner
def bfs_planner(initial_state, goal_state):
    """Breadth-First Search planner"""
    queue = deque()
    queue.append((initial_state, []))  # (state, plan)
    visited = []

    while queue:
        state, plan = queue.popleft()
        if state in visited:
            continue
        visited.append(state)

        if goal_satisfied(state, goal_state):
            return plan, len(visited)

        for action in get_possible_actions(state):
            new_state = apply_action(state, action)
            if new_state is not None:
                queue.append((new_state, plan + [action]))

    return None, len(visited)


# Run the Planner
plan, states_explored = bfs_planner(initial_state, goal_state)

print("Plan found:" if plan else "No plan found")
if plan:
    for i, step in enumerate(plan, 1):
        print(f"{i}. {step}")
print(f"States explored: {states_explored}")

# Let's try with heuristic Search
def heuristic(state, goal):
    """Estimate number of actions left to reach the goal"""
    h = 0
    # Count books not on their goal shelves
    for (book, loc) in goal.get("At", set()):
        if (book, loc) not in state.get("At", set()):
            h += 1
    # Count requested books not delivered
    for (book, user) in goal.get("Delivered", set()):
        if (book, user) not in state.get("Delivered", set()):
            h += 1
    return h

# A* Planner
def a_star_planner(initial_state, goal_state):
    """A* search for Library Robot"""
    open_list = []
    counter = count()  # unique sequence count
    heapq.heappush(open_list, (heuristic(initial_state, goal_state), 0, next(counter), initial_state, []))
    closed_list = []

    while open_list:
        f, g, _, state, plan = heapq.heappop(open_list)

        if goal_satisfied(state, goal_state):
            return plan, len(closed_list)

        if state in closed_list:
            continue
        closed_list.append(state)

        for action in get_possible_actions(state):
            new_state = apply_action(state, action)
            if new_state is not None:
                new_g = g + 1
                new_f = new_g + heuristic(new_state, goal_state)
                heapq.heappush(open_list, (new_f, new_g, next(counter), new_state, plan + [action]))

    return None, len(closed_list)

# Run A* Planner
plan, states_explored = a_star_planner(initial_state, goal_state)

print("Plan found:" if plan else "No plan found")
if plan:
    for i, step in enumerate(plan, 1):
        print(f"{i}. {step}")
print(f"States explored: {states_explored}")
