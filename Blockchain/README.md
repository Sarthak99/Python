**Welcome to the Blockchain project !!**  
This project has the basic components of [building a blockchain](https://github.com/Sarthak99/Python/blob/master/Blockchain/blockchain.py)  in python, creating an [hypothetical cryptocurrency](https://github.com/Sarthak99/Python/blob/master/Blockchain/satocoins.py) and [smart contracts]() in a blockchain.


### Build a basic blockchain
Below are some the code fragments to demonstrate the implementation of few important parts. The entire blockchain has been implemented in python and the interfacing has been done by flask framework. The [imports](https://github.com/Sarthak99/Python/blob/f98622e1be38546e80cc77894106311cb7f2af9f/Blockchain/blockchain.py#L6-L9) defined are necessary for implementing the APIs and hashing algo.  
***
[**create_block**](https://github.com/Sarthak99/Python/blob/b502d6c0ccdaba3cbabb81c9db9d59248ba0af22/Blockchain/blockchain.py#L36-L39) will define the structure of a basic block
```
block = {'index': len(self.chain)+1,
         'timestamp': str(datetime.datetime.now()),
         'proof': proof,
         'previous_hash': previous_hash}
```  
index = defines the position of the block in the chain  
timestamp = defines when the block was created  
proof = the puzzle result to define that a particular block has been mined  
previous_hash = the encrypted hash value to define the link in the chain  

The [**proof**](https://github.com/Sarthak99/Python/blob/b502d6c0ccdaba3cbabb81c9db9d59248ba0af22/Blockchain/blockchain.py#L51)  of a block is a puzzle that a miner must solve to add the transactions from the mempool into the block and encrypt it.  
```  hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()  ```  
The above operation of ```new_proof**2 - previous**2``` is the puzzle miners have to solve and once a value of the proof is obtained, it will be verified against the target set to find the [golden nonce](https://www.blockchain-council.org/blockchain/what-is-a-golden-nonce-and-what-is-its-usage-in-blockchain/).  
The proof in its arithmetical form is actually converted to a 64-hexa digit value by passing through a SHA256 generator. The code ```if hash_operation[:4] == '0000':``` is the hypothetical target defined here for golden nonce and the hash value will be compared against this.  
***
The next part would be to verify that the chain to which the block is being mined is a valid one. The method [is_chain_valid](https://github.com/Sarthak99/Python/blob/b502d6c0ccdaba3cbabb81c9db9d59248ba0af22/Blockchain/blockchain.py#L64-L78) will do that verification by a two-step process:  
* verify the cryptographical link is a valid one i.e. the _previous_hash_ of the current block is equal to the actual hash of the previous  
```if block['previous_hash'] != self.hash(previous_block):```  
* compare the proof of (n-1) and n block proof to solve the puzzle and see if the hash is still under the defined target  
``` hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()```  
``` if hash_operation[:4] != '0000': ```  

The [endpoints/interfaces](https://github.com/Sarthak99/Python/blob/f98622e1be38546e80cc77894106311cb7f2af9f/Blockchain/blockchain.py#L91-L120) will work as below:  
* _/mine_block_ will let an user mine a new block.  
* _/get_chain_ will fetch the entire chain for display.  
* _/i_valid_ will verify if the entire chain, blocks and the cryptographical links are valid.


**!!_Documentation in progress_!!**   
<img src = "http://horticulture.tg.nic.in/img/work-in-progress-wip.jpg" width=220 height=200>
