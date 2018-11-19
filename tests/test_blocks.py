import smerkle


def test_mine_block():
	block = smerkle.Block(smerkle.ROOT_HASH, 1000)
	block.mine()
	assert block.hash is not None
	block.verify()

def test_blockchain():
	blockchain = smerkle.BlockChain()
	assert len(blockchain.blocks) == 1
	genesis_block = blockchain.blocks.values()[0]
	assert genesis_block.prev_blockhash == smerkle.block.ROOT_HASH
	assert genesis_block.height == 0
	assert genesis_block.hash == blockchain.blocks.keys()[0]
	blockchain.mine(20)


def test_address():
	account = smerkle.Account('test')
	assert account.address == '1HKqKTMpBTZZ8H5zcqYEWYBaaWELrDEXeE'
