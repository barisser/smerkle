"""
Elements of a block

previous block hash
nonce
block hash
difficulty
timestamp
block_number
fees
reward



n * 32 + n * -1.44 * ln(p) / ln(2) / 8 bytes
where n is the number of elements
and p is the false positive rate
"""
import smerkle.bloom as bloom
import smerkle.tree as tree

import datetime
import hashlib
import time

import ecdsa
import networkx as nx
import pybitcoin

MAX_ELEMENTS = 2*10**4
ERROR_RATE = 10**-9
SMT_DEPTH = 256

ROOT_HASH = '0000000000000000000000000000000000000000000000000000000000000000'
STARTING_DIFFICULTY = 1

BLOCK_PERIOD = 1
BLOCK_DIFFULTY_LOOKBACK = 5
DIFFICULTY_RECALCULATION_PERIOD = 5 # every 10 blocks


class Account:
    def __init__(self, secret):
        self.secret = secret
        self.privkey = pybitcoin.BitcoinPrivateKey.from_passphrase(secret)
        self.pubkey = self.privkey.public_key().to_hex()
        self.address = self.privkey.public_key().address()


class Transaction:
    def __init__(self, sender, to, coin_id, blockhash):
        self.sender = sender
        self.to = to
        self.coin_id = coin_id
        self.blockhash = blockhash
        self.id = None

    def sign(self, privkey):
        return


def pow(difficulty, *args):
    b = hashlib.sha256(":".join(map(str, args)).encode()).digest()
    r = 0
    for x in b:
        r = r * 256 + int(ord(x))
    return r <= 115792089237316195423570985008687907853269984665640564039457584007913129639936 / difficulty, r



class Block:
    def __init__(self, prev_blockhash, difficulty):
        self.prev_blockhash = prev_blockhash

        self.tree = tree.SMT(max_depth=SMT_DEPTH)
        self.bloom_filter = bloom.BF(MAX_ELEMENTS, ERROR_RATE)
        self.difficulty = difficulty
        self.nonce = None
        self.hash = None
        self.timestamp = None
        self.height = None

    def add_tx(self, transaction):
        self.tree.add_to_leaf(value, position)


    def add_tx_filter(self, transaction_signature):
        self.bloom_filter.add(transaction_signature)

    def verify(self):
        params = [self.tree.root, hashlib.sha256(self.bloom_filter.to_string().encode()).hexdigest(), self.difficulty, self.nonce, self.timestamp]
        passes, blockhash = pow(self.difficulty, *params)
        if not passes and self.hash == blockhash:
            raise Exception("Invalid Block.")
        return blockhash

    def mine(self, max_n=None):
        assert self.prev_blockhash is not None
        self.timestamp = int(time.time() * 1000) / 1000.0
        nonce = 0
        passed = False
        params = [self.tree.root, hashlib.sha256(self.bloom_filter.to_string().encode()).hexdigest(), self.difficulty, self.nonce, self.timestamp]
        while not passed or (max_n is not None and nonce < max_n):
            nonce += 1
            params[3] = nonce
            passed, r = pow(self.difficulty, params)
            if passed:
                print("Difficulty reached: " + str(115792089237316195423570985008687907853269984665640564039457584007913129639936/r))
                self.hash = hashlib.sha256(":".join(map(str, params)).encode()).hexdigest()
                self.nonce = nonce
                print("solved block difficulty {0} with hash {1}".format(self.difficulty, self.hash))

        return passed


    def serialize(self):
        return


class BlockChain:
    def __init__(self):
        self.blocks = {}
        self.graph = nx.DiGraph()
        self.last_blockhash = None
        self.next_block = None
        self.last_block_height = -1
        self.next_difficulty = 1 # TODO
        self.last_difficulty_calculation = 0

        self.add_genesis_block()

    def decide_difficulty(self):
        """
        For a given last block, look at the N previous blocks.
        Compare their timestamps...
        """
        dt = 0
        n = 0

        if self.last_difficulty_calculation + DIFFICULTY_RECALCULATION_PERIOD > self.last_block_height:
            return

        nextblock = self.last_blockhash
        for i in range(BLOCK_DIFFULTY_LOOKBACK):
            parent = self.blocks[nextblock].prev_blockhash
            if parent == ROOT_HASH:
                break
            n += 1
            dt += self.blocks[nextblock].timestamp - self.blocks[parent].timestamp
        if n > 0:
            self.last_difficulty_calculation = self.last_block_height
            avg_time_per_block = dt / float(n)
            self.next_difficulty = self.next_difficulty * (BLOCK_PERIOD / avg_time_per_block)
            print("New difficulty = {0}".format(self.next_difficulty))

    def add_genesis_block(self):
        genesis = Block(ROOT_HASH, STARTING_DIFFICULTY)
        genesis.height = 0
        genesis.mine()
        self.blocks[genesis.hash] = genesis
        self.graph.add_node(genesis.hash)
        self.last_blockhash = genesis.hash
        self.last_block_height = 0

    def add_block(self, block):
        assert block.prev_blockhash in self.blocks or block.prev_blockhash == ROOT_HASH
        self.last_block_height += 1
        block.height = self.last_block_height
        print("Adding Block {0} at height {1}".format(block.hash, block.height))
        self.blocks[block.hash] = block
        self.graph.add_edge(block.prev_blockhash, block.hash)
        self.last_blockhash = block.hash
        self.next_block = None


    def mine(self, n=1):
        for _ in range(n):
            if self.next_block is None:
                self.next_block = Block(self.last_blockhash, self.next_difficulty)

            passed = self.next_block.mine()
            if passed:
                self.add_block(self.next_block)
                #import pdb;pdb.set_trace()
                self.decide_difficulty()
