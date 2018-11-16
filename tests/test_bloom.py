import smerkle


def test_bloom_filter():
	n = 10**4
	p = 10**-6
	bf = smerkle.BF(n, p)
	bf.add('value')

	for i in range(1, n):
		bf.add(str(i))

	for i in range(1, n):
		assert bf.check(str(i))

	for i in range(n, int(n + (1 / p) / 1000)):
		assert not bf.check(str(i))

	root = bf.to_string()
	barray = bf.array
	# bf.from_string(root)
	# assert bf.to_string() == root
	# for i in range(len(bf.array)):
	# 	assert bf.array[i] == barray[i]

	# for i in range(n):
	# 	assert bf.check(str(i))

	# for i in range(n, int(n + (1 / p) / 1000)):
	# 	assert not bf.check(str(i))
