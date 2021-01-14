import json
from typing import List
from queue import PriorityQueue, Queue
from matplotlib.patches import ConnectionPatch
from src.DiGraph import DiGraph
from src.GraphAlgoInterface import GraphAlgoInterface
from src.GraphInterface import GraphInterface
import matplotlib.pyplot as plt
import numpy as np


class GraphAlgo(GraphAlgoInterface):
    """This abstract class represents the algorithms of a graph."""

    def __init__(self, graph: DiGraph = None):
        if graph is None:
            self.graph = DiGraph()
        self.graph_algo = graph

    def get_graph(self) -> GraphInterface:
        """
        :return: the directed graph on which the algorithm works on.
        """
        return self.graph_algo

    def load_from_json(self, file_name: str) -> bool:
        """
        Loads a graph from a json file.
        @param file_name: The path to the json file
        @returns True if the loading was successful, False o.w.
        """
        try:
            with open(file_name, "r") as file:
                graph = DiGraph()
                load = json.load(file)
                for node in load.get("Nodes"):
                    key = node.get("id")
                    pos = None
                    if node.get("pos") is not None:
                        node_pos = node.get("pos").split(",")
                        x = node_pos[0]
                        y = node_pos[1]
                        z = node_pos[2]
                        pos = (x, y, z)
                    graph.add_node(key, pos)
                for edge in load.get("Edges"):
                    graph.add_edge(edge.get("src"), edge.get("dest"), edge.get("w"))
            self.graph_algo = graph
            return True
        except IOError as e:
            print(e)
            return False

    def save_to_json(self, file_name: str) -> bool:
        """
        Saves the graph in JSON format to a file
        @param file_name: The path to the out file
        @return: True if the save was successful, False o.w.
        """
        Nodes = []
        Edges = []
        for node in self.graph_algo.get_all_v():
            nodes = {"id": node}
            Nodes.append(nodes)
            node_out = self.graph_algo.all_out_edges_of_node(node)
            edges_keys = self.graph_algo.all_out_edges_of_node(node).keys()
            for dest in edges_keys:
                edges = {"src": node, "dest": dest, "w": node_out.get(dest)}
                Edges.append(edges)
        ans = {"Nodes": Nodes, "Edges": Edges}
        try:
            with open(file_name, "w") as file:
                json.dump(ans, file)
                return True
        except IOError as e:
            print(e)
            return False

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        """
        Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm
        @param id1: The start node id
        @param id2: The end node id
        @return: The distance of the path, a list of the nodes ids that the path goes through

        Notes:
        If there is no path between id1 and id2, or one of them dose not exist the function returns (float('inf'),[])
        More info:
        https://en.wikipedia.org/wiki/Dijkstra's_algorithm
        """
        path_list = []
        path_size = float("inf")
        node2 = self.graph_algo.get_node(id2)
        nodes = self.graph_algo.get_all_v()
        if not nodes.__contains__(id1) or not nodes.__contains__(id2):
            return path_size, path_list
        if id1 == id2:
            path_size = 0
            path_list.append(id1)
            return path_size, path_list
        self.dijkstra(id1)
        path_size = node2.get_weight()
        if path_size != -1:
            path_list.insert(0, id2)
            prev_node = node2.get_parent()
            while prev_node != id1:
                path_list.insert(0, prev_node)
                prev_node = self.graph_algo.get_node(prev_node).get_parent()
            path_list.insert(0, id1)
        else:
            path_size = float("inf")
        return path_size, path_list

    def connected_component(self, id1: int) -> list:
        """
        Finds the Strongly Connected Component(SCC) that node id1 is a part of.
        @param id1: The node id
        @return: The list of nodes in the SCC

        Notes:
        If the graph is None or id1 is not in the graph, the function should return an empty list []
        """
        _list = []
        _dict = {}
        if self.get_graph().get_all_v().__contains__(id1):
            dfs_list = self.dfs(id1)
            self.replace_dicts()
            for node_id in dfs_list:
                _dict[node_id] = "visited"
            _list = self.dfs(id1, _dict)
            self.replace_dicts()
        return _list

    def connected_components(self) -> List[list]:
        """
        Finds all the Strongly Connected Component(SCC) in the graph.
        @return: The list all SCC

        Notes:
        If the graph is None the function should return an empty list []
        """
        self.reset_nodes()
        _list = []
        for node_id in self.graph_algo.get_all_v().keys():
            if self.graph_algo.get_node(node_id).get_info() != "black":
                list_of_scc = self.connected_component(node_id)
                for key in list_of_scc:
                    self.graph_algo.get_node(key).set_info("black")
                _list.append(list_of_scc)
        return _list

    def plot_graph(self) -> None:
        """
        Plots the graph.
        If the nodes have a position, the nodes will be placed there.
        Otherwise, they will be placed in a random but elegant manner.
        @return: None
        """
        fig, ax = plt.subplots(figsize=(8, 6))
        for key in self.graph_algo.get_all_v().keys():
            node = self.graph_algo.get_node(key)
            x, y, z = node.get_pos()
            src = np.array([x, y])
            ax.annotate(node.get_key(), (x, y), color="black")
            for id2 in self.graph_algo.all_out_edges_of_node(key).keys():
                x, y, z = self.graph_algo.get_node(id2).get_pos()
                dest = np.array([x, y])
                ax.plot([src[0], dest[0]], [src[1], dest[1]], "o", color="red")
                ax.add_artist(ConnectionPatch(src, dest, "data", "data", shrinkA=5, shrinkB=5, arrowstyle="->", color="grey"))
        plt.title("Graph")
        plt.show()

    def reset_nodes(self):
        """
        Resets the weight, parent and info of each node in the graph
        @return:
        """
        nodes = self.graph_algo.get_all_v()
        for key in nodes.keys():
            node = self.graph_algo.get_node(key)
            node.set_weight(-1)
            node.set_parent(-1)
            node.set_info("white")

    def dijkstra(self, src: int):
        """
        The method checks what the shortest path from src to each node in the graph
        and updates the weight(path_size) and the parent(path_list) of each node
        @param src:
        @return:
        """
        queue = PriorityQueue()
        self.reset_nodes()
        queue.put(src)
        self.graph_algo.get_node(src).set_weight(0)
        while not queue.empty():
            current = queue.get()
            curr_node = self.graph_algo.get_node(current)
            curr_node.set_info("black")
            for neighbor in self.graph_algo.all_out_edges_of_node(current).keys():
                next_node = self.graph_algo.get_node(neighbor)
                wei = self.graph_algo.get_edge(current, neighbor)
                if next_node.get_info() != "black":
                    queue.put(next_node.get_key())
                    if next_node.get_weight() > curr_node.get_weight() + wei or next_node.get_weight() == -1:
                        next_node.set_weight(curr_node.get_weight() + wei)
                        next_node.set_parent(curr_node.get_key())

                if next_node.get_weight() > curr_node.get_weight() + wei:
                    next_node.set_weight(curr_node.get_weight() + wei)
                    next_node.set_parent(curr_node.get_key())
                    queue.put(next_node.get_key())

    def replace_dicts(self):
        """
        Replaces between the dicts: the HashIn is the HashOut
        and the HashOut is the HashIn
        @return:
        """
        for key in self.graph_algo.get_all_v():
            node = self.graph_algo.get_node(key)
            _in = node.get_hashIn()
            _out = node.get_hashOut()
            node.set_hashIn(_out)
            node.set_hashOut(_in)

    def dfs(self, node_id: int, _dict: dict = None) -> list:
        """
        Returns a list of the nodes that connect to the node_id
        and mark them as "visited"
        @param node_id:
        @param _dict:
        @return:
        """
        self.reset_nodes()
        _list = [node_id]
        queue = Queue()
        queue.put(node_id)
        self.graph_algo.get_node(node_id).set_info("visited")
        while not queue.empty():
            curr_node = queue.get()
            for id2 in self.get_graph().all_out_edges_of_node(curr_node):
                node = self.graph_algo.get_node(id2)
                if node.get_info() != "visited":
                    queue.put(id2)
                    node.set_info("visited")
                    if _dict is None or _dict.get(id2) == "visited":
                        _list.append(id2)
        return _list
