import main

graph = {
    'A': [('B', 2), ('C', 1), ('D', 7)],
    'B': [('E', 5), ('F', 3)],
    'C': [('B', 4), ('F', 6)],
    'D': [('G', 8), ('C', 2)],
    'E': [('H', 3)],
    'F': [('H', 2), ('I', 4)],
    'G': [('J', 4)],
    'H': [('I', 1), ('J', 2)],
    'I': [('J', 3)],
    'J': []
}

path, cost = main.uniform_cost_search(graph, 'A', 'J');
print(f"Cheapest path: {path}, Cost of cheapest path: {cost}")