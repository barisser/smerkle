import random
import time

import smerkle

def test_creation_of_tree():
	tree = smerkle.SMT()

	for i in range(100):
		m = i * 130
		tree.add_node(m, 40, str(i) + 'hello')
	assert tree.root() == '45832e75f073304e6dc4e885f6e4f1f11d004949e633777c7cef48a8609448ce'

	for i in range(100):
		m = i * 130
		path = tree.path(m, 40)
		assert smerkle.verify_path(path, tree.root())
		assert tree.hash(path[-1][0]+path[-1][1]) == tree.root()

	dump = tree.to_string()
	tree2 = smerkle.SMT(dump=dump)
	assert tree2.root() == tree.root()


def test_memberships():
	tree = smerkle.SMT()

	for i in range(100):
		depth = 64
		n = random.randint(0, 2**depth-1)
		value = str(i)
		path = tree.add_node(n, depth, value)
		assert tree.path(n, depth) == path
		assert smerkle.infer_position(path, tree.root()) == (depth, n)



def test_perf():
	tree = smerkle.SMT()

	start = time.time()
	for i in range(20):
		n = random.randint(0, 2**63)
		tree.add_node(n, 63, str(i) + 'test')
	duration = time.time() - start
	print(duration)

	dump = tree.sparse_dump()
	assert len(dump) == 20 # number of elements exactly!
