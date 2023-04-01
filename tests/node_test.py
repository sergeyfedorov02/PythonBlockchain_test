import sys
import random
import json

sys.path.append('../blockchain')

import blockchain.node as node
import blockchain.block as block


def test_node_init():
    for i in range(100):
        server_id = random.randint(1, 3)
        new_node = node.Node(server_id)

        assert new_node is not None

        assert new_node.server_id == server_id
        assert new_node.block_index is None
        assert len(new_node.blocks_array) == 0


def test_create_genesis():
    for i in range(100):
        genesis_node = node.create_genesis()

        assert genesis_node is not None
        assert type(genesis_node) == str

        python_object = json.loads(genesis_node)
        genesis_generated_by = python_object['This block generated by Node '][0]
        genesis_index = int(python_object['index'])
        genesis_hash = python_object['hash']
        genesis_prev_hash = python_object['prev_hash']
        genesis_data = python_object['data']

        assert genesis_generated_by == -1
        assert genesis_index == 0
        assert genesis_hash[-4:] == "0000"
        assert genesis_prev_hash == 'GENESIS'
        assert len(genesis_data) == 256


def test_block_handler_genesis():
    server_id = random.randint(1, 3)
    current_node = node.Node(server_id)
    genesis_block = node.create_genesis()

    assert current_node.server_id == server_id
    assert current_node.block_index == None
    assert len(current_node.blocks_array) == 0

    current_node.block_handler(genesis_block)

    assert current_node.server_id == server_id
    assert current_node.block_index == 0
    assert len(current_node.blocks_array) == 1


def test_block_handler_not_genesis():
    node_server_id = random.randint(1, 3)
    current_node = node.Node(node_server_id)

    for i in range(100):
        block_server_id = random.randint(1, 3)
        last_index = random.randint(1, 1000)
        prev_hash = 'This is Last block in Node'
        nonce_type = random.randint(1, 3)

        last_block_in_node_array = block.create_new_block(last_index, prev_hash, nonce_type,
                                                          block_server_id).block_to_json()

        current_node.block_index = last_index
        current_node.blocks_array.append(last_block_in_node_array)

        answer_false = current_node.block_handler(last_block_in_node_array)
        assert answer_false == False

        last_block_array_length = len(current_node.blocks_array)

        new_index = random.randint(1, 1000)
        new_prev_hash = 'This is new Received block'
        new_received_block = block.create_new_block(new_index, new_prev_hash, nonce_type,
                                                          block_server_id).block_to_json()

        answer_block_handler = current_node.block_handler(new_received_block)

        if new_index > last_index:
            assert answer_block_handler == True
            assert current_node.block_index == new_index
            assert len(current_node.blocks_array) == last_block_array_length + 1
        else:
            assert answer_block_handler == False
            assert current_node.block_index == last_index
            assert len(current_node.blocks_array) == last_block_array_length



