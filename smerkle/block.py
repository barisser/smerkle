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

import networkx as nx

MAX_ELEMENTS = 2*10**4
ERROR_RATE = 10**-9
SMT_DEPTH = 256

ROOT_HASH = '0000000000000000000000000000000000000000000000000000000000000000'
STARTING_DIFFICULTY = 1

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

    def add_tx(tx_id):
        self.tree.add_to_next_leaf(tx_id)

    def add_tx_filter(transaction_signature):
        self.bloom_filter.add(transaction_signature)

    def verify(self):
        params = [self.tree.root, hashlib.sha256(self.bloom_filter.to_string().encode()).hexdigest(), self.difficulty, self.nonce, self.timestamp]
        passes, blockhash = pow(self.difficulty, *params)
        if not passes and self.hash == blockhash:
            raise Exception("Invalid Block.")
        return blockhash

    def mine(self):
        self.timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S') # UTC
        nonce = 0
        passed = False
        params = [self.tree.root, hashlib.sha256(self.bloom_filter.to_string().encode()).hexdigest(), self.difficulty, self.nonce, self.timestamp]
        while not passed:
            nonce += 1
            params[3] = nonce
            passed, r = pow(self.difficulty, params)
            if passed:
                print("Difficulty reached: " + str(115792089237316195423570985008687907853269984665640564039457584007913129639936/r))
                self.hash = hashlib.sha256(":".join(map(str, params)).encode()).hexdigest()
                print("solved block difficulty {0} with hash {1}".format(self.difficulty, self.hash))


    def serialize(self):
        return


class BlockChain:
    def __init__(self):
        self.blocks = {}
        self.graph = nx.DiGraph()
        self.add_genesis_block()

    def add_genesis_block(self):
        genesis = Block(ROOT_HASH, STARTING_DIFFICULTY)
        genesis.mine()
        self.blocks[genesis.hash] = genesis


    def add_block(self, block):
        assert block.prev_blockhash in self.blocks or block.prev_blockhash == ROOT_HASH
        self.blocks[block.hash] = block
        self.graph.add_edge(block.prev_blockhash, block.hash)


    # def mine(self, last_block=None):
    #     if last_block is None:
    #         last_block = 
    #     return
