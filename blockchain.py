from time import time
import json, hashlib, requests
from uuid import uuid4
from urllib.parse import urlparse
from flask import Flask, jsonify, request

class Blockchain:
    def __init__(self):
        self.nodes = set()
        self.chain = []
        self.all_transactions = []
        self.create_block(previous_block_hash='1', signature=100)

    def create_block(self, signature, previous_block_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.all_transactions,
            'signature': signature,
            'previous_block_hash': previous_block_hash or self.get_hash(self.chain[-1]),
        }
        self.all_transactions = []
        self.chain.append(block)
        return block

    def create_transaction(self, sender, recipient, amount):
        self.all_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.previous_block['index'] + 1

    @property
    def previous_block(self):
        return self.chain[-1]

    @staticmethod
    def get_hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def pow(self, previous_block):
        previous_signature = previous_block['signature']
        previous_hash = self.get_hash(previous_block)
        signature = 0
        while self.validate(previous_signature, signature, previous_hash) is False:
            signature += 1
        return signature

    @staticmethod
    def validate(previous_signature, signature, previous_hash):
        encoded_signature = f'{previous_signature}{signature}{previous_hash}'.encode()
        signature_hash = hashlib.sha256(encoded_signature).hexdigest()
        return signature_hash[:4] == "0000"


app = Flask(__name__)

node_address = str(uuid4()).replace('-', '')

blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    previous_block = blockchain.previous_block
    signature = blockchain.pow(previous_block)
    blockchain.create_transaction(
        sender="0",
        recipient=node_address,
        amount=1,
    )
    previous_block_hash = blockchain.get_hash(previous_block)
    block = blockchain.create_block(signature, previous_block_hash)
    response_data = {
        'message': "Mined a new block!",
        'index': block['index'],
        'transactions': block['transactions'],
        'signature': block['signature'],
        'previous_block_hash': block['previous_block_hash'],
    }
    return jsonify(response_data), 200

@app.route('/chain', methods=['GET'])
def get_chain():
    response_data = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response_data), 200

@app.route('/', methods=['GET'])
def home():
    return "Welcome to Building Your Own Blockchain!<br><br>Go to <a href='/chain'>/chain</a> url..", 200

if __name__ == '__main__':
    from argparse import ArgumentParser
    argp = ArgumentParser()
    argp.add_argument('-p', '--port', default=8000, type=int, help='port for server to listen')
    args = argp.parse_args()
    port = args.port
    app.run(host='0.0.0.0', port=port)
