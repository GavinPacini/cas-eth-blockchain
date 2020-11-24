# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import hashlib
import json
import pprint
from time import time, ctime
from random import randint, seed


class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.difficulty = "00000"

        self.new_block(previous_hash="A blockchain made for ETH's CAS in Applied Information Technology")

    def new_block(self, previous_hash=None):
        current_hash, proof = self.proof_of_work(previous_hash)

        block = {
            'index': len(self.chain) + 1,
            'timestamp': ctime(time()),
            'transactions': self.pending_transactions,
            'proof': proof,
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
        proof = 0
        seed()

        if current_hash is None:
            max_randint = pow(10, len(self.difficulty)) * 100
            temp_hash = ""
            while not temp_hash.startswith(self.difficulty):
                temp_hash = self.hash(self.chain[-1], proof)
                proof = randint(0, max_randint)

            current_hash = temp_hash

        return current_hash, proof

    @staticmethod
    def hash(block, proof):
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()

        block_string += str(proof).encode()

        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()

        return hex_hash


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    pp = pprint.PrettyPrinter(indent=4)

    blockchain = Blockchain()
    print("genesis block:")
    pp.pprint(blockchain.last_block)

    t1 = blockchain.new_transaction("Gavin", "Gino", '10 BTC')
    t2 = blockchain.new_transaction("Gavin", "Manu", '20 BTC')
    print("mining...")
    blockchain.new_block()
    pp.pprint(blockchain.last_block)

    t3 = blockchain.new_transaction("Gino", "Gavin", '5 BTC')
    t4 = blockchain.new_transaction("Manu", "Gavin", '10 BTC')
    print("mining...")
    blockchain.new_block()
    pp.pprint(blockchain.last_block)

    print("Full Blockchain:")
    pp.pprint(blockchain.chain)
