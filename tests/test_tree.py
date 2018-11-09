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

