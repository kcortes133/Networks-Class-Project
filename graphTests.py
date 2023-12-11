import unittest, editMonarchKG


# check how many nodes in original graph and after filtering
# compare node number to nodes in edge file
# compare source nodes to destination nodes

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here

class NodesTest(unittest.TestCase):
    def checkNumNodes(self):
        editMonarchKG.readNodes()

if __name__ == '__main__':
    unittest.main()
