import copy
import hashlib
import random
import time

import smerkle

def test_creation_of_tree():
	tree = smerkle.SMT()

	for i in range(100):
		m = i * 130
		tree.add_node(m, 40, str(i) + 'hello')
	assert tree.root() == '6da37977c157bbe64d16d521c9dd31c31856242ed5b9c6d0ab42f9603f332569'

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
	depth = 64
	
	for i in range(100):	
		n = random.randint(0, 2**depth-1)
		value = str(i)
		path = tree.add_node(n, depth, value)
		assert len(path) == depth + 1 # these are all occupied
		assert tree.path(n, depth) == path
		assert smerkle.verify_membership(value, path, tree.root())
		assert not smerkle.verify_nonmembership(path, tree.root(), depth)
		assert not smerkle.verify_membership(value, path, 'asdasd')
		assert not smerkle.verify_membership('asdasd', path, tree.root())
		fakepath = copy.copy(path)
		fakepath[3][0] = hashlib.sha256('qweqw'.encode()).hexdigest()
		assert not smerkle.verify_membership(value, fakepath, tree.root())
#		assert smerkle.infer_position(path, tree.root()) == (depth, n)

	for i in range(1000):
		m = random.randint(0, 2**depth-1)
		path = tree.path(m, depth)
		assert smerkle.verify_path(path, tree.root())
		assert smerkle.verify_nonmembership(path, tree.root(), depth)

		import pdb;pdb.set_trace()


	

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
