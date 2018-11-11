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
import bloom
import tree

MAX_ELEMENTS = 2*10**4
ERROR_RATE = 10**-9

class Strand: # single input/output component of a transaction
    def __init__(self, sender, to, amt):
        self.sender = sender
        self.to = to
        self.amt = amt

    def sign(self, sender_privkey):
        return


class Transaction:
    def __init__(self, inputs, outputs, blockhash):
        self.inputs = inputs # strands
        self.outputs = outputs
        self.blockhash = blockhash

    def sign(self, privkey):
        return

    def txhash(self):
        return self.txhash

class Block:
    def __init__(self, n, prev_block, difficulty):
        self.n = n
        self.prev_block = prev_block

        self.tree = tree.SMT()
        self.bloom_filter = bloom.BF(MAX_ELEMENTS, ERROR_RATE)
        self.difficulty = difficulty
        self.hash = None

    def add_tx_tree(transaction):
        tx_hash = transaction.txhash()
        self.tree.add_to_next_leaf(tx_hash)


    def add_tx_filter(transaction_signature):
        self.bloom_filter.add(transaction_signature)


    def serialize(self):
        return

