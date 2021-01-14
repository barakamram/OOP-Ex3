import json
import random
from src.GraphInterface import GraphInterface


class Node:
    """This abstract class represents a vertex."""

    def __init__(self, key: int, pos: tuple = None):
        self.key = key
        self.pos = pos
        self.weight = 0
        self.info = ""
        self.parent = None
        self.hashIn = {}
        self.hashOut = {}

    def get_key(self) -> int:
        """
        return the ID of the node
        :return: The ID of the node
        """
        return self.key

    def get_pos(self):
        """
        Returns the position of the node
        if the there is no position to the node it will update in random location
        :return: The position of the node
        """
        if self.pos is None:
            x = random.uniform(32.001, 32.999)
            y = random.uniform(35.001, 35.999)
            self.pos = (x, y, 0)
        return self.pos

    def get_weight(self) -> float:
        """
        Returns the distance
        :return: The distance
        """
        return self.weight

    def set_weight(self, w: float):
        """
        Sets the distance
        :param w:
        :return:
        """
        self.weight = w

    def get_info(self) -> str:
        """
        Returns the info of the node
        :return: The info of the node
        """
        return self.info

    def set_info(self, s: str):
        """
        Sets the info of the node
        :param s:
        :return:
        """
        self.info = s

    def get_parent(self):
        """
        Returns the parent of the node
        :return: The parent of the node
        """
        return self.parent

    def set_parent(self, node_id: int):
        """
        Sets the parent of the node
        :param node_id:
        :return:
        """
        self.parent = node_id

    def get_hashIn(self) -> dict:
        """
        Returns the incoming edges list
        :return: The incoming edges list
        """
        return self.hashIn

    def add_hashIn(self, node_id: int, weight: float) -> bool:
        """
        Adds the node_id to the incoming edges list with the weight of the edge
        :param node_id:
        :param weight:
        :return: True if the node added successfully False if not
        """
        if self.key is not node_id:
            if self.hashIn.get(node_id):
                if self.hashIn.get(node_id) != weight:
                    self.hashIn[node_id] = weight
                    return True
            self.hashIn.setdefault(node_id, weight)
        return False

    def remove_hashIn(self, node_id: int) -> bool:
        """
        Removes node from the incoming edges list
        :param node_id:
        :return: True if the node removed successfully False if not
        """
        if self.hashIn.get(node_id):
            del self.hashIn[node_id]
            return True
        return False

    def set_hashIn(self, _dict: dict):
        """
        Sets incoming edges list
        :param _dict:
        :return:
        """
        self.hashIn = _dict

    def get_hashOut(self) -> dict:
        """
        Returns the outgoing edges list
        :return: The outgoing edges list
        """
        return self.hashOut

    def add_hashOut(self, node_id: int, weight: float) -> bool:
        """
        Adds the node_id to the outgoing edges list with the weight of the edge
        :param node_id:
        :param weight:
        :return: True if the node added successfully False if not
        """
        if self.key is not node_id:
            if self.hashOut.get(node_id):
                if self.hashOut.get(node_id) != weight:
                    self.hashOut[node_id] = weight
                    return True
            self.hashOut.setdefault(node_id, weight)
        return False

    def remove_hashOut(self, node_id: int) -> bool:
        """
        Removes node from the outgoing edges list
        :param node_id:
        :return: True if the node removed successfully False if not
        """
        if self.hashOut.get(node_id):
            del self.hashOut[node_id]
            return True
        return False

    def set_hashOut(self, _dict: dict):
        """
        Sets outgoing edges list
        :param _dict:
        :return:
        """
        self.hashOut = _dict

    def __eq__(self, other):
        if self is None:
            return False
        if other is None or other.__class__ != self.__class__:
            return False
        return self.get_hashIn().keys().__eq__(other.get_hashIn().keys()) and self.get_hashOut().keys().__eq__(
            other.get_hashOut().keys())

    def __str__(self):
        return self.key

    def __repr__(self):
        return repr((self.key, self.pos))

    def __lt__(self, other):
        return self.weight < other.weight


class DiGraph(GraphInterface):
    """This abstract class represents a directed weighted graph."""

    def __init__(self):
        self.nodes = {}
        self.num_of_edges = 0
        self.mc = 0

    def get_node(self, node_id: int) -> Node:
        """
        Returns the ID of the node
        @param node_id:
        @return:The ID of the node
        """
        return self.nodes.get(node_id)

    def get_edge(self, id1: int, id2: int) -> float:
        """
        Returns the weight of the edge between id1 to id2
        @param id1:
        @param id2:
        @return: The weight of the edge
        """
        if not self.has_edge(id1, id2):
            return -1
        return self.get_node(id1).get_hashOut().get(id2)

    def has_edge(self, id1: int, id2: int) -> bool:
        """
        Returns if there is an edge between id1 to id2
        @param id1:
        @param id2:
        @return: True if there is an edge False if not
        """
        return not self.get_node(id1).get_hashOut().get(id2) is None

    def v_size(self) -> int:
        """
        Returns the number of vertices in this graph
        @return: The number of vertices in this graph
        """
        if self is None:
            return 0
        return len(self.nodes)

    def e_size(self) -> int:
        """
        Returns the number of edges in this graph
        @return: The number of edges in this graph
        """
        if self is None:
            return 0
        return self.num_of_edges

    def get_all_v(self) -> dict:
        """
        return a dictionary of all the nodes in the Graph, each node is represented using a pair
        (node_id, node_data)
        """
        return self.nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        """
        return a dictionary of all the nodes connected to (into) node_id ,
        each node is represented using a pair (other_node_id, weight)
        """
        return self.get_node(id1).get_hashIn()

    def all_out_edges_of_node(self, id1: int) -> dict:
        """
        return a dictionary of all the nodes connected from node_id , each node is represented using a pair
        (other_node_id, weight)
        """
        return self.get_node(id1).get_hashOut()

    def get_mc(self) -> int:
        """
        Returns the current version of this graph,
        on every change in the graph state - the MC should be increased
        @return: The current version of this graph.
        """
        return self.mc

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        """
        Adds a node to the graph.
        @param node_id: The node ID
        @param pos: The position of the node
        @return: True if the node was added successfully, False o.w.

        Note: if the node id already exists the node will not be added
        """
        if not self.nodes.__contains__(node_id):
            node = Node(node_id, pos)
            self.nodes[node_id] = node
            self.mc += 1
            return True
        return False

    def remove_node(self, node_id: int) -> bool:
        """
        Removes a node from the graph.
        @param node_id: The node ID
        @return: True if the node was removed successfully, False o.w.

        Note: if the node id does not exists the function will do nothing
        """
        if self.nodes.__contains__(node_id):
            hash_in = self.get_node(node_id).get_hashIn()
            hash_out = self.get_node(node_id).get_hashOut()
            for node in hash_in.keys():
                self.get_node(node).remove_hashOut(node_id)
                self.num_of_edges -= 1
            for node in hash_out.keys():
                self.get_node(node).remove_hashIn(node_id)
                self.num_of_edges -= 1
            self.nodes.pop(node_id)
            self.mc += 1
            return True
        return False

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        """
        Adds an edge to the graph.
        @param id1: The start node of the edge
        @param id2: The end node of the edge
        @param weight: The weight of the edge
        @return: True if the edge was added successfully, False o.w.

        Note: If the edge already exists or one of the nodes dose not exists the functions will do nothing
        """
        if self.nodes.__contains__(id1) and self.nodes.__contains__(id2):
            if not self.has_edge(id1, id2) and id1 != id2:
                self.get_node(id1).add_hashOut(id2, weight)
                self.get_node(id2).add_hashIn(id1, weight)
                self.num_of_edges += 1
                self.mc += 1
                return True
        return False

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        """
        Removes an edge from the graph.
        @param node_id1: The start node of the edge
        @param node_id2: The end node of the edge
        @return: True if the edge was removed successfully, False o.w.

        Note: If such an edge does not exists the function will do nothing
        """
        if self.nodes.__contains__(node_id1) and self.nodes.__contains__(node_id2):
            if self.has_edge(node_id1, node_id2):
                self.get_node(node_id1).remove_hashOut(node_id2)
                self.get_node(node_id2).remove_hashIn(node_id1)
                self.num_of_edges -= 1
                self.mc += 1
                return True
        return False

    def __eq__(self, other):
        if other is None or self.__class__ != other.__class__:
            return False
        return self.nodes.__eq__(other.nodes)

    def __repr__(self):
        _info = []
        _dict = {}
        _str = f"Graph: |V| = {len(self.nodes)}, |E| = {self.num_of_edges}"
        for node_id in self.nodes.keys():
            _dict[node_id] = f"{node_id}: |edges out| {len(self.all_out_edges_of_node(node_id))} |edges in| {len(self.all_in_edges_of_node(node_id))}"
        _info.append(_str)
        _info.append(repr(_dict))
        graph = "\n".join(_info)
        return graph

