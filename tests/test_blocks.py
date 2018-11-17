import smerkle


def test_mine_block():
	block = smerkle.Block(smerkle.ROOT_HASH, 1000)
	block.mine()
	assert block.hash is not None
	block.verify()

def test_blockchain():
	blockchain = smerkle.BlockChain()