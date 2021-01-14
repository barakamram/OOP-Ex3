import unittest as test
from src.DiGraph import DiGraph


class TestDiGraph(test.TestCase):

    def test_add_node(self):
        g = DiGraph()
        for i in range(0, 10):
            g.add_node(i)
        self.assertEqual(10, g.v_size())
        self.assertFalse(g.add_node(9))
        self.assertEqual(10, g.v_size())
        self.assertTrue(g.add_node(10))
        self.assertEqual(11, g.v_size())
        self.assertEqual(11, g.get_mc())

    def test_remove_node(self):
        g = DiGraph()
        for i in range(0, 10):
            g.add_node(i)
        g.add_edge(2, 3, 1)
        g.add_edge(2, 6, 1)
        g.add_edge(2, 4, 1)
        g.add_edge(1, 2, 1)
        g.add_edge(5, 4, 1)
        g.add_edge(2, 5, 1)
        g.remove_node(2)
        self.assertEqual(g.get_all_v().get(2), None)
        self.assertEqual(0, len(g.all_out_edges_of_node(1)))
        self.assertEqual(9, g.v_size())
        self.assertEqual(1, g.e_size())
        self.assertTrue(g.remove_node(9))
        self.assertIsNone(g.get_all_v().get(9))
        self.assertEqual(8, g.v_size())
        self.assertEqual(1, g.e_size())
        self.assertEqual(18, g.get_mc())

    def test_add_edge(self):
        g = DiGraph()
        for i in range(0, 10):
            g.add_node(i)
        for i in range(0, 10):
            g.add_edge(i, 9 - i, 0.5)
        self.assertFalse(g.add_edge(5, 10, 3))
        self.assertEqual(10, g.e_size())
        self.assertFalse(g.add_edge(0, 9, 1))
        self.assertEqual(10, g.e_size())
        self.assertFalse(g.add_edge(5, 5, 2))
        self.assertEqual(20, g.get_mc())

    def test_remove_edge(self):
        g = DiGraph()
        for i in range(0, 10):
            g.add_node(i)
        for i in range(0, 10):
            g.add_edge(i, 9 - i, 0.5)
        g.remove_edge(1, 8)
        self.assertEqual(9, g.e_size())
        self.assertEqual(21, g.get_mc())
        self.assertTrue(0 in g.all_out_edges_of_node(9).keys())
        self.assertTrue(1 in g.all_out_edges_of_node(8).keys())
        self.assertFalse(8 in g.all_out_edges_of_node(1).keys())

    def test_v_size(self):
        g = DiGraph()
        for i in range(0, 10):
            g.add_node(i)
        self.assertEqual(10, g.v_size())

    def test_e_size(self):
        g = DiGraph()
        for i in range(0, 10):
            g.add_node(i)
        for i in range(0, 10):
            g.add_edge(i, 9 - i, 0.5)
        self.assertEqual(10, g.e_size())

    def test_get_all_v(self):
        g = DiGraph()
        for i in range(0, 10):
            g.add_node(i)
        flag = True
        for i in range(0, 10):
            if i not in g.get_all_v().keys():
                flag = False
            self.assertTrue(flag)

    def test_all_in_edges_of_node(self):
        g = DiGraph()
        for i in range(0, 10):
            g.add_node(i)
        g.add_edge(2, 3, 1)
        g.add_edge(2, 6, 1)
        g.add_edge(2, 4, 1)
        g.add_edge(1, 2, 1)
        g.add_edge(5, 4, 1)
        g.add_edge(2, 5, 1)
        self.assertEqual(2, len(g.all_in_edges_of_node(4)))
        g.add_edge(1, 4, 1)
        self.assertEqual(3, len(g.all_in_edges_of_node(4)))
        g.add_edge(1, 4, 1)
        self.assertEqual(3, len(g.all_in_edges_of_node(4)))
        g.remove_edge(1, 4)
        self.assertEqual(2, len(g.all_in_edges_of_node(4)))

    def test_all_out_edges_of_node(self):
        g = DiGraph()
        for i in range(0, 10):
            g.add_node(i)
        g.add_edge(2, 3, 1)
        g.add_edge(2, 6, 1)
        g.add_edge(2, 4, 1)
        g.add_edge(1, 2, 1)
        g.add_edge(5, 4, 1)
        g.add_edge(2, 5, 1)
        self.assertEqual(4, len(g.all_out_edges_of_node(2)))
        g.remove_edge(2, 3)
        self.assertEqual(1, len(g.all_out_edges_of_node(5)))
        g.add_edge(5, 6, 1)
        self.assertEqual(2, len(g.all_out_edges_of_node(5)))
        g.add_edge(5, 6, 1)
        self.assertEqual(2, len(g.all_out_edges_of_node(5)))
        g.remove_edge(5, 6)
        self.assertEqual(1, len(g.all_out_edges_of_node(5)))

    def test_mc(self):
        g = DiGraph()
        for i in range(0, 10):
            g.add_node(i)
        g.add_edge(2, 3, 1)
        g.add_edge(2, 6, 1)
        g.add_edge(2, 4, 1)
        g.add_edge(1, 2, 1)
        g.add_edge(5, 4, 1)
        g.add_edge(2, 5, 1)
        self.assertEqual(16, g.get_mc())
        g.add_edge(2, 5, 1)
        self.assertEqual(16, g.get_mc())
        g.add_node(8)
        self.assertEqual(16, g.get_mc())
        g.remove_edge(2, 6)
        self.assertEqual(17, g.get_mc())
        g.remove_edge(2, 1)
        self.assertEqual(17, g.get_mc())
        g.remove_node(2)
        self.assertEqual(18, g.get_mc())
        g.remove_node(2)
        self.assertEqual(18, g.get_mc())

    def test_get_edge(self):
        g = DiGraph()
        for i in range(0, 5):
            g.add_node(i)
        g.add_edge(4, 2, 1)
        g.add_edge(4, 2, 0.5)
        self.assertFalse(g.add_edge(2, 2, 1))
        self.assertEqual(1, g.get_edge(4, 2))
        self.assertEqual(-1, g.get_edge(4, 1))
        self.assertEqual(-1, g.get_edge(2, 4))


if __name__ == '__main__':
    test.main()