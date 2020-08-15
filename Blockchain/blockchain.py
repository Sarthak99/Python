#Creating a blockchain

#Install flask: pip install Flask

#Libraries for build the blocks and providing user interface
import datetime
import hashlib
import json
from flask import Flask, jsonify


# =============================================================================
# 1.Create the blockchain
# =============================================================================

class BlockChain:

    #Define the chain for the class and create an instance of it
    def __init__(self):
        self.chain = []
        # Define the Genesis block with a hardcoded proof and '0' previous_hash
        self.create_block(proof=1, previous_hash='0')

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
                 'previous_hash': previous_hash}
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
            if block['previous_hash'] != self.hash(block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

# =============================================================================
# 2.Mining the Blockchain
# =============================================================================

#Create the web API using Flask
app = Flask(__name__)

#Instantiate a blockchain
BLOCKCHAIN = BlockChain()

#Mining a new block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = BLOCKCHAIN.get_previous_block()
    previous_proof = previous_block['proof']    #Extract the previous proof in the chain
    previous_hash = BLOCKCHAIN.hash(previous_block)  #Extract the previous hash for the new block
    proof = BLOCKCHAIN.proof_of_work(previous_proof)
    new_block = BLOCKCHAIN.create_block(proof, previous_hash)
    response = {'messsage':'Block has been successfully mined!!',
                'index': new_block['index'],
                'timestamp':new_block['timestamp'],
                'proof': new_block['proof'],
                'previous_hash':new_block['previous_hash']}
    return jsonify(response), 200

#Fetch the entire block
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain':BLOCKCHAIN.chain,
                'lenght':len(BLOCKCHAIN.chain)}
    return jsonify(response), 200

#Running the web API
app.run(host='127.0.0.1', port=5005) #Change host to 0.0.0.0 if you want external access on blockchain to be mined.
