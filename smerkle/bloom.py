"""
Bloom Filter Implementation

https://en.wikipedia.org/wiki/Bloom_filter
k number of hash functions
m length of filter
n number of elements
p probability of false positive


m = n * -1.44 * ln(p) / ln(2)
k = -1 * ln(p) / ln(2)
"""
import base64
import hashlib
import math
import zlib



class BF:
	def __init__(self, max_elements, error_rate):
		self.error_rate = error_rate
		self.n_elements = 0
		self.max_elements = max_elements
		self.m = math.ceil(max_elements * -1.44 * math.log(error_rate) / math.log(2))
		self.array = [0] * self.m

		self.k = math.ceil(-1 * math.log(error_rate) / math.log(2))
		self.hash_functions = []
		for y in range(self.k):
			h = " " * y
			hf = (lambda h: lambda x: hashlib.sha256((x + h).encode()).hexdigest())(h)
			self.hash_functions.append(hf)

	def compute_signature(self, value):
		sig = [0] * self.m
		for i in range(self.k):
			hv = int(self.hash_functions[i](value), 16) % self.m
			sig[hv] = 1
		return sig

	def add(self, value):
		self.n_elements += 1
		if self.n_elements > self.max_elements:
			raise Exception("Cannot exceed max elements in Bloom Filter.")
		
		for i in range(self.k):
			hv = int(self.hash_functions[i](value), 16) % self.m
			self.array[hv] = 1

	def check(self, value):
		for i in range(self.k):
			hv = int(self.hash_functions[i](value), 16) % self.m
			if self.array[hv] == 0:
				return False
		return True

	def to_string(self):
		i = int("".join([str(x) for x in self.array]), 2)
		j = hex(i).encode()
		c = zlib.compress(j)
		return base64.b64encode(c)

	def from_string(self, s):
		c = base64.b64decode(s)
		j = zlib.decompress(c)
		i = int(j.decode(), 16)
		b = format(i, "b")
		b = "0" * (len(self.array) - len(b)) + b
		self.array = [int(x) for x in b]
		