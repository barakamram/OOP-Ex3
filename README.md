# OOP-Ex3

### Made by : Barak Amram & Liroy Melamed.

### DiGraph:<br/>
**This abstract class represents a directed weighted graph.**<br/>

| function | Description |
| --- | --- |
| get_node | Returns the ID of the node. |
| get_edge | Returns the weight of the edge between id1 to id2. |
| v_size |  Returns the number of vertices in the graph. |
| e_size | Returns the number of edges in the graph. |
| get_all_v | Return a dictionary of all the nodes in the Graph, each node is represented using a pair (node_id, node_data). |
| all_in_edges_of_node | Returns a dictionary of all the nodes connected to (into) node_id , each node is represented using a pair (other_node_id, weight). |
| all_out_edges_of_node | Returns a dictionary of all the nodes connected from node_id , each node is represented using a pair (other_node_id, weight). |
| get_mc |  Returns the current version of this graph, on every change in the graph state - the MC should be increased. |
| add_node | Adds a node to the graph |
| remove_node | Removes a node from the graph. |
| add_edge | Adds an edge to the graph. |
| remove_edge | Removes an edge from the graph. |



### GraphAlgo:<br/>

**This abstract class represents the algorithms of a graph.**<br/>

| function | Description |
| --- | --- |
| __init__ | Initialize the graph. |
| get_graph | Returns the directed graph on which the algorithm works on. |
| load_from_json | Loads a graph from a json file. |
| save_to_json | Saves the graph in JSON format to a file |
| shortest_path | Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm |
| connected_component | Finds the Strongly Connected Component(SCC) that node id1 is a part of. |
| connected_components | Finds all the Strongly Connected Component(SCC) in the graph. |
| plot_graph | Plots the graph |
