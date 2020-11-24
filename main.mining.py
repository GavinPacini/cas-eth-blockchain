import hashlib
import json
import pprint
from time import time, ctime
from random import randint, seed


class Blockchain(object):

    def __init__(self, difficulty):
        self.chain = []
        self.pending_transactions = []
        self.difficulty = difficulty

        self.new_block(previous_hash="A blockchain made for ETHZ's CAS in Applied Information Technology")

    def new_block(self, previous_hash=None):
        current_hash, nonce = self.proof_of_work(previous_hash)

        block = {
            'index': len(self.chain) + 1,
            'timestamp': ctime(time()),
            'transactions': self.pending_transactions,
            'nonce': nonce,
            'previous_hash': current_hash
        }

        self.pending_transactions = []
        self.chain.append(block)

        return block

    @property
    def last_block(self):
        return self.chain[-1]

    def new_transaction(self, sender, recipient, amount):
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }

        self.pending_transactions.append(transaction)
        return self.last_block['index'] + 1

    def proof_of_work(self, previous_hash):
        current_hash = previous_hash
        nonce = 0
        seed()

        if current_hash is None:
            max_randint = pow(10, len(self.difficulty)) * 100
            temp_hash = ""
            while not temp_hash.startswith(self.difficulty):
                temp_hash = self.hash(self.chain[-1], nonce)
                nonce = randint(0, max_randint)

            current_hash = temp_hash

        return current_hash, nonce

    @staticmethod
    def hash(block, nonce):
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()

        block_string += str(nonce).encode()

        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()

        return hex_hash


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Setup a "pretty printer" to make our outputs easier to read
    pp = pprint.PrettyPrinter(indent=4)

    # Create an instance of our blockchain, with a specified difficulty
    blockchain = Blockchain("0000")
    print("genesis block:")
    pp.pprint(blockchain.last_block)

    # Add some transactions
    t1 = blockchain.new_transaction("Gavin", "Gino", '10 BTC')
    t2 = blockchain.new_transaction("Gavin", "Manu", '20 BTC')
    # Mine a new block
    print("mining...")
    blockchain.new_block()
    pp.pprint(blockchain.last_block)

    t3 = blockchain.new_transaction("Gino", "Gavin", '5 BTC')
    t4 = blockchain.new_transaction("Manu", "Gavin", '10 BTC')
    print("mining...")
    blockchain.new_block()
    pp.pprint(blockchain.last_block)

    # Print our complete blockchain
    print("Full Blockchain:")
    pp.pprint(blockchain.chain)
