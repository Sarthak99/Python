#Creating a CrytpoCurrency "satocoins"

#Install flask: pip install Flask

#Libraries for build the blocks and providing user interface
import datetime
import hashlib
import json
from uuid import uuid4
from urllib.parse import urlparse
from flask import Flask, jsonify, request
import requests



# =============================================================================
# 1.Create the blockchain
# =============================================================================

class BlockChain:

    #Define the chain for the class and create an instance of it
    def __init__(self):
        self.chain = []
        #object to store the crypto transactions
        self.transactions = []
        # Define the Genesis block with a hardcoded proof and '0' previous_hash
        self.create_block(proof=1, previous_hash='0')
        self.nodes = set()

#define the block and it's attributes
# =============================================================================
# block {index: index/position of the block in the chain
#        timestamp: time of the block created,
#        proof: proof that the current block has been mined,
#        previous_hash: hash value of the previous block
#       }
# proof:This will be defined by the proof_of_work method
#         and hence the block will be created when it is mined.
# previous_hash: this will be hash value of the previous mined block
# =============================================================================
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain)+1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions': self.transactions}
        self.transactions = [] #Empty the object to mine new transactions
        self.chain.append(block)
        return block
# Fetch the previous block of the chain
    def get_previous_block(self):
        return self.chain[-1]

# Define and verify the proof of work by considering the previous_hash
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

# Create a hash of the block by converting entire block to a json
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

# Verify every link in the chain is valid and the current block has a valid proof.
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1        
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

# Create a new method to add crypto transactions to a block
    def add_transactions(self, sender, receiver, amount):
        transaction = {'sender': sender,
                       'recevier': receiver,
                       'amount': amount}
        self.transactions.append(transaction)
        # Now find the previously mined block and
        # return the next block index where the transactions need to be mined
        previous_block = self.get_previous_block()
        return previous_block['index']+1

#Create a new method to track all the nodes
    def add_nodes(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

# =============================================================================
# A new method to verify the if the current chain needs
# to be replaced by the longest chain in the network
# This is the consensus protocol for the integrity of the decentralized blockchain
# =============================================================================
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            # Get the response of each chain from all nodes in the network by making a get request on /get_chain
            response = requests.get(f'http://{node}/get_chain')
            length = response.json()['length']
            chain = response.json()['chain']
            # verify the length of chain with self chain and the validity of the node chain
            if length > max_length and self.is_chain_valid(chain):
                max_length = length
                longest_chain = chain
        # If the longest chain has been updated in the network, replace self chain with the longest chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False

# =============================================================================
# 2.Mining the Blockchain
# =============================================================================

#Create the web API using Flask
APP = Flask(__name__)

#Create an address for the node on port 5000
NODE_ADDRESS = str(uuid4()).replace('-', '')

#Instantiate a blockchain
BLOCKCHAIN = BlockChain()

#Mining a new block
@APP.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = BLOCKCHAIN.get_previous_block()
    previous_proof = previous_block['proof']    #Extract the previous proof in the chain
    previous_hash = BLOCKCHAIN.hash(previous_block)  #Extract the previous hash for the new block
    proof = BLOCKCHAIN.proof_of_work(previous_proof)
    BLOCKCHAIN.add_transactions(sender=NODE_ADDRESS, receiver='Elon Musk', amount=10)
    new_block = BLOCKCHAIN.create_block(proof, previous_hash)
    response = {'messsage':'Block has been successfully mined!!',
                'index': new_block['index'],
                'timestamp':new_block['timestamp'],
                'proof': new_block['proof'],
                'previous_hash':new_block['previous_hash'],
                'transactions':new_block['transactions']}
    return jsonify(response), 200

#Fetch the entire chain
@APP.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain':BLOCKCHAIN.chain,
                'length':len(BLOCKCHAIN.chain)}
    return jsonify(response), 200

#Add a new transaction to the blockchain
@APP.route('/add_transaction', methods = ['POST'])
def add_transactions_to_block():
    json = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all(key in json for key in transaction_keys):
        return 'Some elements of the transasctions are missing.', 400
    index = BLOCKCHAIN.add_transactions(sender=json['sender'],
                                        receiver=json['receiver'],
                                        amount=json['amount'])
    response = {'message':f'transaction has been created and will be added to block{index}'}
    return jsonify(response), 201

#Fetch the chain validity
@APP.route('/is_valid', methods=['GET'])
def is_valid():
    is_valid = BLOCKCHAIN.is_chain_valid(BLOCKCHAIN.chain)
    if is_valid:
        response = {'message':'Blockchain is in a valid state'}
    else:
        response = {'message':'!!!ALERT!!! Blockchain is invalid !!!!'}
    return jsonify(response), 200

# =============================================================================
# 3.Decentralizing the Blockchain
# =============================================================================

#Connecting to new nodes
@APP.route('/connect_node', methods=['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return "No Nodes", 400
    for node in nodes:
        BLOCKCHAIN.add_nodes(node)
    response = {'message':'All the nodes are now connected. The satocoin Blockchain now contains following nodes:',
                'total_nodes':list(BLOCKCHAIN.nodes)}
    return jsonify(response), 201

@APP.route('/replace_chain', methods=['GET'])
def replace_chain():
    is_chain_replaced = BLOCKCHAIN.replace_chain()
    if is_chain_replaced:
        repsonse = {'message:':'The nodes were out of sync.The chain was replacedby the longest chain',
                    'new_chain':BLOCKCHAIN.chain}
    else:
        repsonse = {'message:':'Current chain is the longest.No replacement necessary.',
                    'current_chain':BLOCKCHAIN.chain}
    return jsonify(repsonse), 200

#Running the web API
#Change host to 0.0.0.0 if you want external access on blockchain to be mined.
APP.run(host='127.0.0.1', port=5006)