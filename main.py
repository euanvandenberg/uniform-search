# The below example implements a uniform-cost search. Imagine A, B and C are towns, and the numbers represent some distance between them.
# There are two key points about the uniform-cost search:
# 1. It searches to find the lowest cost path.
# 2. It finds the lowest cost path by traversing the node with the lowest cost so far. So after finding 'A', has a connection with 'B', and 'C'. It traverses 'B', first as it only has a cost of 1. This ensures the path returned always has the lowest cost, as if a node which finds a path to the goal is discovered, all other lower cost paths are evaluated first.

# heapq library contains a priority queue algorithm. As oppose to a queue which is FIFO, a priority queue dequeues items based on their priority. The priority is the lowest cost value.
import heapq

# A graph is a data structure consisting of nodes (or vertices) and edges. If you were to visualise this, it would be as an imaginary 2D area showing positions of nodes and edges connecting these nodes.
# A node (or vertex) is simply a point on this 2D area. There is no more precise definition of it than this. What is being represented by this node depends on the type of data being used. For example a node could represent a town or a computer server. Here, 'A', 'B' and 'C' are the nodes.
# An edge is a connection between two nodes. It represents something connecting the two nodes. For example it may show two towns are connected.
# A weight is an optional value which is assigned to an edge. What is meant by it again depends on the data being used. It could represent the distance between two towns or the amount of fuel used to get from one town to another. It may have a zero value if the edge has no cost.
# If a graph is directed, edges have a direction. For example you can only go from A to B, not B to A. This example is directed, 'B' doesn't have an edge with 'A'.
# If a graph is undirected, edges have no direction, You can go from A to B and B to A. 
# The graph below is represented as a dictionary where each node has a list of (connectedNode, cost) tuples.
graph = {
    'A': [('B', 1), ('C', 5)],
    'B': [('C', 2)],
    'C': []
}

# This function implements the uniform-cost search, utilising the priority queue. It takes the graph data structure (what the search is traversing), the start (which node the search starts on) and the goal (which node it is trying to reach). In a nutshell it checks the edges of the first node, sees which nodes it's connected to, adds those nodes to the queue to be checked adding the path to get there and adding the culmulative cost to get there, checks which node in the queue has the lowest cost, checks the edges of the lowest cost node to see which nodes it's connected to and continues this process until the node it pops from the queue is the goal node it's trying to reach. This node will contain the path to get to it and the culmulative cost to get to it. Any other nodes which may either have a path to the goal node or be the goal node themselves will have a higher culmulative cost, as the lower cost nodes are always popped first. So every cheaper path is evaluated before returning the final path.
def uniform_cost_search(graph, start, goal):
    
    # Priority queue to store (cost, current_node, path) tuples. The queue is essentially a to-do list of places we haven’t explored yet, and each entry has information on the cost so far and the path taken so far. So it tracks how much it has costed to get to the nodes in the queue, and the path it has taken to get there.
    queue = []

    # The empty queue has the tuple pushed onto it which is the starting node. The tuple's first value is a cost of 0 as this is the starting position (the cost is the priority the queue considers when dequeuing an item, with the lowest dequeued first). The tuple's second value is the starting node and the third is the path traversed so far which is currently just the starting node.
    heapq.heappush(queue, (0, start, [start]))

    # Initialises a new set which represents the nodes visited so far. This means no node which has been evaluated before gets evaluated again. The edges it contains are only checked once.
    visited = set()

    # While the queue has a value, this runs. Meaning it evaluates nodes added to the queue until it finds the lowest cost path to return or there are no further connected nodes to check and the goal node hasn't been reached.
    while queue:
        # heapq.heappop(queue) returns the node with the smallest cost. This removes it from the queue ensuring the edges of it are only evaluated once. As the lowest cost element is popped from the queue to be evaulated first, even if a node in the queue is the goal node or contains a path to the goal node, it won't be returned unless it's the lowest cost path. If the popped node is the goal node, the remaining nodes must have a higher cost.
        # On the first iteration, this is the tuple representing the starting position. current_cost = 0, current_node = 'A' and path = ['A']. The queue is empty after popping.
        # On the second iteration, current_cost = 1, current_node = 'B' and path = ['A', 'B']. The queue contains [(5, 'C', ['A', 'C']). A path might have been identified, but the cost is higher than the current_node, so it must be evaluated first.
        # On the third iteration, current_cost = 3, current_node = 'C' and path = ['A', 'B', 'C']. The queue contains [(5, 'C', ['A', 'C']). A path has been identified which is cheaper than 5, the path A -> C will not be returned.
        current_cost, current_node, path = heapq.heappop(queue)

        # If we have reached the goal, return the path and the culmulative cost. It will be the cheapest.
        # On the first iteration, 'A' != 'C', so it doesn't return.
        # On the second iteration, 'B' != 'C', so it doesn't return.
        # On the third iteration, 'C' == 'C', so it does return. The node which would continue to be evaluated as just a connected node with further edges to explore, is the goal node.
        if current_node == goal:
            return (path, current_cost)

        # If the current_node is in the visited set, go back to the start of the while loop. The edges of it and all connected nodes will already have been added to the queue and checked or are still waiting to be checked.
        # On the first iteration, 'A', is not in the visited set so doesn't reach the continue keyword.
        # On the second iteration, 'B', is not in the visited set so doesn't reach the continue keyword.
        if current_node in visited:
            continue
        
        # Add the current node to the set of visited nodes.
        # On the first iteration, 'A', is added to the visited set. After, visited = ['A']
        # On the second iteration, 'B', is added to the visited set. After, visited = ['A', 'B']
        visited.add(current_node)

        # graph[current_node] retrieves the value of the node key, which is the list of tuples denoting the connected nodes and weight of the edge to get to that connected node.
        for connectedNode, cost in graph[current_node]:
            # For each tuple, it first checks if the connectedNode has previously been visited. If it hasn't, it continues. If it has, that connectedNode can be skipped.
            # On the first iteration of the while loop, on the first iteration of the for loop, connectedNode = 'B' which is not in the visited set, so it goes to heapq.push.
            # On the first iteration of the while loop, on the second iteration of the for loop, connectedNode = 'C' which is not in the visited set, so it goes to heapq.push.
            # On the second iteration of the while loop, on the first iteration of the for loop, connectedNode = 'C' which is not in the visited set, so it goes to heapq.push.
            if connectedNode not in visited:
                # The queue has a new tuple pushed onto it, which is a node connected to the current node that needs its edges checked for any further connections. Any node which is the current_node is either the starting node or one which is connected to the starting node directly or indirectly. The first value, is the combination of the cost to get to the current_node plus the cost of the connectedNode. It's essentially building a culmulative cost for all the nodes on the path. It also adds the entire path of the current_node to the new value being added to the queue, appending the current node to it. So the queue contains nodes which need checked further, along with the culmulative cost and path it took to get there. So at the end it can show the full path and the cost of that path.
                # On the first iteration of the while loop, on the first iteration of the for loop, the single tuple value pushed to the empty queue is (1, 'B', ['A', 'B'])
                # On the first iteration of the while loop, on the second iteration of the for loop, the second tuple pushed to the queue is (5, 'C', ['A', 'C'])
                # On the second iteration of the while loop, on the first iteration of the for loop, the tuple value pushed to the queue which now only contains (5, 'C', ['A', 'C']), is (3, 'C', ['A', 'B', 'C'])
                heapq.heappush(queue, (current_cost + cost, connectedNode, path + [connectedNode]))
    return None

if __name__ == "__main__":
    path, cost = uniform_cost_search(graph, 'A', 'C')
    print(f"Cheapest path: {path}, Cost of cheapest path: {cost}")