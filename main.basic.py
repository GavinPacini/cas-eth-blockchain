import hashlib
import json
import pprint
from time import time, ctime, sleep


class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.pending_transactions = []

        self.new_block(previous_hash="A blockchain made for ETHZ's CAS in Applied Information Technology", nonce=100)

    def new_block(self, nonce, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': ctime(time()),
            'transactions': self.pending_transactions,
            'nonce': nonce,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
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

    @staticmethod
    def hash(block):
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()

        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()

        return hex_hash


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # Setup a "pretty printer" to make our outputs easier to read
    pp = pprint.PrettyPrinter(indent=4)

    # Create an instance of our blockchain
    blockchain = Blockchain()
    # Add some transactions
    t1 = blockchain.new_transaction("Gavin", "Gino", '10 BTC')
    t2 = blockchain.new_transaction("Gavin", "Manu", '20 BTC')
    # Wait, then generate a new block
    sleep(5)
    blockchain.new_block(12345)

    t3 = blockchain.new_transaction("Gino", "Gavin", '5 BTC')
    t4 = blockchain.new_transaction("Manu", "Gavin", '10 BTC')
    sleep(5)
    blockchain.new_block(6789)

    # Print our complete blockchain
    print("Full Blockchain:")
    pp.pprint(blockchain.chain)
