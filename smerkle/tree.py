import base64
import hashlib
import json
import zlib

DEFAULT_HASH_FUNCTION = lambda x: hashlib.sha256(str(x).encode()).hexdigest()

def int_to_binarray(x, d):
	"""
	Finds the pathway for the X'th item in row D using zero based indexing.
	"""
	m = [int(s) for s in bin(x)[2:]]
	return [0] * (d - len(m)) + m

def binarray_to_int(x):
	s = 0
	for k in x:
		s = s * 2 + k
	return s

def verify_path(path, hashfunction=DEFAULT_HASH_FUNCTION):
	for i in range(0, len(path) - 1):
		left = path[i][0]
		right = path[i][1]
		expected_parent = hashfunction(left + right)
		if expected_parent not in path[i+1]:
			return False
	return True


class SMT:
	def __init__(self, max_depth=256, hashfunction=DEFAULT_HASH_FUNCTION, dump=None):
		self.hashes = {}
		self.n_elements = 0
		self.max_depth = max_depth
		self.hash = hashfunction
		
		self.empty_hashes = dict()
		self.empty_hashes[max_depth] = self.hash(max_depth)

		# cache empty hashes for all depths
		for i in range(1, max_depth):
			j = max_depth - i
			self.empty_hashes[j] = self.hash(self.empty_hashes[j+1] * 2)

		if dump is not None:
			self.from_string(dump)



	def read_hash(self, coordinate):
		return self.hashes.get(tuple(coordinate), self.empty_hashes[len(coordinate)])


	def add_node(self, n, depth, value):
		"""
		Adds to an arbitrary, not-necessarily leaf node at the N'th node at depth.
		Also performs hashes recurively upward.
		You are not allowed to modify a node that is the parent of another from the outside,
		otherwise you will break the relationship.  Existing hashes can only be overwritten
		when working upwards recursively.
		"""
		m = int_to_binarray(n, depth)
		if tuple(m) in self.hashes:
			raise Exception("Cannot directly modify occupied hashes.")

		self.hashes[tuple(m)] = self.hash(value)

		while len(m) > 0:
			m = m[:-1]
			left = m + [0]
			right = m + [1]
			lhash = self.read_hash(left)
			rhash = self.read_hash(right)
			self.hashes[tuple(m)] = self.hash(lhash + rhash)

		self.n_elements += 1

	def add_to_next_leaf(self, value):
		self.add_node(self.n_elements, self.max_depth, value) # technically nodes added at non-leaves make this non-monotonic, but OK.

	def add_to_leaf(self, value, position):
		"""
		Adds the hash of value X to leaf node position.
		"""
		self.add_node(position, self.max_depth, value)

	def add_node_set(self, nodeset):
		"""
		Adds a list of nodes and computes more efficiently.
		A list of nodes is composed of a list of [n, depth, value]
		"""
		# TODO
		return


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


	def sparse_dump(self):
		"""
		Dump the minimal amount of data necessary to reconstruct the FULL tree.
		"""
		dump = {}
		for coord in self.hashes.keys():
			intcoord = binarray_to_int(coord)
			if len(coord) + 1 == self.max_depth: # these are child nodes
				dump[intcoord] = self.hashes[coord]
			else:
				left = coord + (0,)
				right = coord + (1,)
				if not left in self.hashes and not right in self.hashes: # this point was defined but not at the bottom layer, should be included in dump
					dump[intcoord] = self.hashes[coord]

		# TODO make this base64 rather than a dict
		return dump

	def to_string(self):
		dump = self.sparse_dump()
		dump['max_depth'] = self.max_depth
		s = str(json.dumps(dump))
		zs = zlib.compress(s)
		return base64.b64encode(zs)

	def from_string(self, dump):
		"""
		Populates the tree from a sparse b64-encoded dump.
		Assumes all data is at leaf nodes.
		"""
		# TODO
		j = base64.b64decode(dump)
		q = zlib.decompress(j)
		r = json.loads(q)

		self.hashes = {}
		self.n_elements = 0

		for k in r:
			if k == 'max_depth':
				self.max_depth = r[k]
			else:
				self.add_to_leaf(r[k], int(k))
				# w = int_to_binarray(int(k), self.max_depth)
				# self.hashes[tuple(w)] = r[k]
				# self.n_elements += 1
