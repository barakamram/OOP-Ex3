import unittest as test
from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo


class TestGraphAlgo(test.TestCase):

    def test_shortest_path(self):
        g = DiGraph()
        for i in range(0, 5):
            g.add_node(i)
        g.add_edge(0, 1, 3)
        g.add_edge(1, 2, 5)
        g.add_edge(0, 2, 10)
        g.add_edge(2, 3, 5)
        g.add_edge(3, 4, 5)
        g.add_edge(0, 4, 19)
        graph = GraphAlgo(g)
        path_size, path_list = graph.shortest_path(0, 4)
        self.assertEqual(path_size, 18)
        self.assertEqual(path_list, [0, 1, 2, 3, 4])
        path_size, path_list = graph.shortest_path(3, 0)
        self.assertEqual(path_size, float("inf"))
        self.assertEqual(path_list, [])
        path_size, path_list = graph.shortest_path(9, 2)
        self.assertEqual(path_size, float("inf"))
        self.assertEqual(path_list, [])
        graph.plot_graph()

    def test_connected_component(self):
        g = DiGraph()
        for i in range(1, 7):
            g.add_node(i)
        g.add_edge(1, 4, 10)
        g.add_edge(4, 1, 10)
        g.add_edge(1, 5, 10)
        g.add_edge(5, 1, 10)
        g.add_edge(2, 4, 10)
        g.add_edge(3, 2, 10)
        g.add_edge(1, 6, 10)
        g.add_edge(6, 5, 10)
        g.add_edge(5, 6, 10)
        g.add_edge(6, 1, 10)
        graph = GraphAlgo(g)
        self.assertEqual(4, len(graph.connected_component(1)))
        self.assertEqual(1, len(graph.connected_component(2)))
        self.assertEqual(0, len(graph.connected_component(10)))
        graph.plot_graph()

    def test_connected_components(self):
        g = DiGraph()
        for i in range(1, 7):
            g.add_node(i)
        g.add_edge(1, 4, 10)
        g.add_edge(4, 1, 10)
        g.add_edge(1, 5, 10)
        g.add_edge(5, 1, 10)
        g.add_edge(2, 3, 10)
        g.add_edge(3, 2, 10)
        g.add_edge(4, 6, 10)
        g.add_edge(6, 5, 10)
        g.add_edge(5, 6, 10)
        g.add_edge(6, 4, 10)
        graph = GraphAlgo(g)
        self.assertEqual(3, len(graph.connected_components()))
        graph.plot_graph()

    def test_plot_graph(self):
        g = DiGraph()
        for i in range(1, 7):
            g.add_node(i)
        g.add_edge(1, 2, 10)
        g.add_edge(2, 1, 10)
        g.add_edge(1, 3, 10)
        g.add_edge(3, 1, 10)
        g.add_edge(2, 4, 10)
        g.add_edge(3, 4, 10)
        g.add_edge(6, 1, 10)
        g.add_edge(4, 5, 10)
        g.add_edge(5, 6, 10)
        g.add_edge(3, 6, 10)
        g.add_edge(6, 5, 10)
        graph = GraphAlgo(g)
        graph.plot_graph()

    def test_load_and_save(self):
        g = DiGraph()
        for i in range(1, 8):
            g.add_node(i)
        g.add_edge(1, 2, 10)
        g.add_edge(2, 1, 10)
        g.add_edge(1, 3, 10)
        g.add_edge(2, 4, 10)
        g.add_edge(3, 4, 10)
        g.add_edge(1, 4, 10)
        g.add_edge(3, 5, 10)
        g.add_edge(5, 6, 10)
        g.add_edge(6, 5, 10)
        _g = g
        graph = GraphAlgo(g)
        file = "json_file"
        self.assertTrue(graph.save_to_json(file))
        self.assertTrue(graph.load_from_json(file))
        self.assertEqual(_g, graph.get_graph())
        graph.plot_graph()


if __name__ == '__main__':
    test.main()