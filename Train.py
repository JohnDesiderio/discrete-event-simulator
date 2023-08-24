"""
This file manages the cargo and train classes.
and stores the definiton for the graph class
to find the shortest path. 
"""
import collections
import heapq
import numpy as np


def shortest_Path(edges: "The preloaded graph of everything", source: " from (str)", dest: " to (str)"):
    # create a weighted DAG - {node:[(cost,neighbour), ...]}
    graph = collections.defaultdict(list)
    for l, r, c in edges:
        graph[l].append((c, r))
    # create a priority queue and hash set to store visited nodes
    queue, visited = [(0, source, [])], set()
    heapq.heapify(queue)
    # traverse graph with BFS
    while queue:
        (cost, node, path) = heapq.heappop(queue)
        # visit the node if it was not visited before
        if node not in visited:
            visited.add(node)
            path = path + [node]
            # hit the dest
            if node == dest:
                return (cost, path)
            # visit neighbours
            for c, neighbour in graph[node]:
                if neighbour not in visited:
                    heapq.heappush(queue, (cost+c, neighbour, path))
    return float("inf")


class Cargo:
    """
    This is the cargo class used to manage all
    instances of cargo. In this class, sim exec
    sets a destination, and the cargo will not 
    be discarded until the simulation ends.
    """
    def __init__(self, current, dest, graph):
        self.dest = dest
        self.current = current
        self.graph = graph
        self.schedule = None

    def calculate_path(self):
        """
        Find the shortest path for cargo to move
        """
        path = shortest_Path(self.graph, self.current, self.dest)
        self.schedule = path[1][1:]


class Train:
    """
    The vehicle to transport the cargo.
    """
    def __init__(self, num, name, size, graph, data, network, seed):
        np.random.seed(seed=seed)
        self.num = num
        self.name = name
        self.current = None
        self.size = size
        self.luggage = []
        self.graph = graph
        self.path = None
        self.time = data
        self.network = network

    def check_cargo(self, env):
        """
        Check the cargo at the train station to see what we can pick up.
        """
        for x in self.current.cargo:
            if len(list(set(self.path[1][1:]) & set(x.schedule))) > 0:
                if len(self.luggage) < self.size:
                    self.luggage.append(x)
        if len(self.luggage) > 0:
            print(f'{env.now}: {self.name} is carrying {len(self.luggage)} cars of cargo')
        for x in self.luggage:
            if x in self.current.cargo:
                self.current.cargo.remove(x)

    def update_cargo(self, env):
        """
        Check the cargo inventory to see what cargo is arrived
        """
        # Remove the current station from the cargo schedule list
        temp = self.current.name
        for x in self.luggage:
            if temp in x.schedule: 
                x.schedule.remove(temp)
        finished = []
        for x in self.luggage:
            if x.schedule == []:
                finished.append(x)
        delivered = 0
        for x in finished:
            delivered += 1 
            self.luggage.remove(x)

        self.current.delivered_cars += delivered
        if delivered > 0:
            print(f'{env.now}: {self.name} delivered {delivered} car(s) of cargo!')

    def drop_cargo_off(self, env):
        """
        This method is for train to drop off cargo that no longer shares
        any destinations along its path. The current train drops it off
        and hopes another train picks it up.
        """
        drop_off = []
        for x in self.luggage:
            if len(list(set(self.path[1][1:]) & set(x.schedule))) == 0:
                if len(x.schedule) > 0:
                    drop_off.append(x)
        if len(drop_off) > 0:
            print(f"{env.now}: {self.name} dropped off {len(drop_off)} cars of cargo at {self.current.name}")
        for x in drop_off:
            self.luggage.remove(x)
            self.current.cargo.append(x) 
