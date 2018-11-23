import random
import time

import smerkle

def test_creation_of_tree():
	tree = smerkle.SMT()

	for i in range(100):
		m = i * 130
		tree.add_node(m, 40, str(i) + 'hello')
	assert tree.root() == '6d85167b8834c4ee42342355ba19493a11797b52090002ece4471b5513112a94'

	for i in range(100):
		m = i * 130
		path = tree.path(m, 40)
		assert smerkle.verify_path(path)
		assert path[-1] == tree.root()

	dump = tree.to_string()
	tree2 = smerkle.SMT(dump=dump)
	assert tree2.root() == tree.root()


def test_perf():
	tree = smerkle.SMT()

	start = time.time()
	for i in range(20):
		n = random.randint(0, 2**254)
		tree.add_node(n, 255, str(i) + 'test')
	duration = time.time() - start
	print(duration)

	dump = tree.sparse_dump()
	assert len(dump) == 20 # number of elements exactly!
