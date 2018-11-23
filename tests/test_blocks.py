import os
import time

import smerkle


def test_mine_block():
	block = smerkle.Block(smerkle.ROOT_HASH, 1000, 0)
	block.mine()
	assert block.hash is not None
	block.verify()
	block_string = block.to_string()

	block2 = smerkle.block_from_string(block_string)
	assert block.to_string() == block2.to_string()


def test_blockchain():
	blockchain = smerkle.BlockChain()
	assert len(blockchain.blocks) == 1
	genesis_block = blockchain.blocks.values()[0]
	assert genesis_block.prev_blockhash == smerkle.block.ROOT_HASH
	assert genesis_block.height == 0
	assert genesis_block.hash == blockchain.blocks.keys()[0]
	blockchain.mine(10)

	folder_path = "./bc_{0}".format(int(time.time()))
	os.system('mkdir {0}'.format(folder_path))
	blockchain.to_path(folder_path)


def test_address():
	account = smerkle.Account('test')
	assert account.address == '1HKqKTMpBTZZ8H5zcqYEWYBaaWELrDEXeE'
