import node
import unittest

class TestNode(unittest.TestCase):
	def setUp(self):
		self.anode = node.Node();	

	def test_we_can_construct_a_node(self):
		self.assertEqual({}, self.anode.connections)
		self.assertEqual({}, self.anode.routingPath)

	def test_addConnection_raise_TypeError(self):
		with self.assertRaises(TypeError):
			self.anode.addConnection(1,12.0)
		with self.assertRaises(TypeError):
			self.anode.addConnection('192.168.0.1','12.0')

	def test_we_can_add_connection_to_the_node(self):
		self.anode.addConnection('192.168.0.1',12.0)
		self.anode.addConnection('192.168.0.2',11.0)
		self.assertEqual({'192.168.0.1':12.0,'192.168.0.2':11.0}, self.anode.connections)

	def test_PathConstrucor_raise_TypeError(self):
		with self.assertRaises(TypeError):
			node.Path(1,12.0)
		with self.assertRaises(TypeError):
			node.Path([],'a')
	
	def test_we_can_add_routingPath_to_the_node(self):
		self.path = node.Path(['192.168.0.4','192.168.0.5','192.168.0.6'],0.2);
		self.anode.addPath('192.168.0.1',self.path)
		self.assertEqual({'192.168.0.1':self.path}, self.anode.routingPath)			

if __name__ == '__main__':
	unittest.main()
