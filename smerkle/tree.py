import hashlib

DEFAULT_HASH_FUNCTION = lambda x: hashlib.sha256(str(x).encode()).hexdigest()

def int_to_binarray(x, d):
	"""
	Finds the pathway for the X'th item in row D using zero based indexing.
	"""
	m = [int(s) for s in bin(x)[2:]]
	return [0] * (d - len(m)) + m


def verify_path(path, hashfunction=DEFAULT_HASH_FUNCTION):
	for i in range(0, len(path) - 1):
		left = path[i][0]
		right = path[i][1]
		expected_parent = hashfunction(left + right)
		if expected_parent not in path[i+1]:
			return False
	return True


class SMT:
	def __init__(self, max_depth=256, hashfunction=DEFAULT_HASH_FUNCTION):
		self.hashes = {}
		self.max_depth = max_depth
		self.hash = hashfunction
		
		self.empty_hashes = dict()
		self.empty_hashes[max_depth] = self.hash(max_depth)

		# cache empty hashes for all depths
		for i in range(1, max_depth):
			j = max_depth - i
			self.empty_hashes[j] = self.hash(self.empty_hashes[j+1] * 2)


	def read_hash(self, coordinate):
		return self.hashes.get(tuple(coordinate), self.empty_hashes[len(coordinate)])


	def add_node(self, n, depth, value):
		"""
		Adds to an arbitrary, not-necessarily leaf node at the N'th node at depth.
		Also performs hashes recurively upward.
		"""
		m = int_to_binarray(n, depth)
		self.hashes[tuple(m)] = self.hash(value)

		while len(m) > 0:
			m = m[:-1]
			left = m + [0]
			right = m + [1]
			lhash = self.read_hash(left)
			rhash = self.read_hash(right)
			self.hashes[tuple(m)] = self.hash(lhash + rhash)


	def path(self, n, depth):
		"""
		Returns a merkle path from n, depth to root.
		The format of the path is an array of [LEFT VALUE, RIGHT VALUE] followed by a single [roothash]
		"""
		m = int_to_binarray(n, depth)
		path = []

		while len(m) > 0:
			m = m[:-1]
			left = m + [0]
			right = m + [1]
			path.append([self.read_hash(left), self.read_hash(right)])
		path.append(self.hashes[()])

		return path

	def root(self):
		return self.hashes[()]
