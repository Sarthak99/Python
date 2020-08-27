**Welcome to the Blockchain project !!**  
This project has the basic components of [building a blockchain](https://github.com/Sarthak99/Python/blob/master/Blockchain/blockchain.py)  in python and creating an [hypothetical cryptocurrency](https://github.com/Sarthak99/Python/blob/master/Blockchain/satocoins.py) in a blockchain.

***

### Build a basic blockchain
Below are some the code fragments to demonstrate the implementation of few important parts. The entire blockchain has been implemented in python and the interfacing has been done by flask framework. The [imports](https://github.com/Sarthak99/Python/blob/f98622e1be38546e80cc77894106311cb7f2af9f/Blockchain/blockchain.py#L6-L9) defined are necessary for implementing the APIs and hashing algo.  
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
The next part would be to verify that the chain to which the block is being mined is a valid one. The method [is_chain_valid](https://github.com/Sarthak99/Python/blob/b502d6c0ccdaba3cbabb81c9db9d59248ba0af22/Blockchain/blockchain.py#L64-L78) will do that verification by a two-step process:  
* verify the cryptographical link is a valid one i.e. the _previous_hash_ of the current block is equal to the actual hash of the previous  
```if block['previous_hash'] != self.hash(previous_block):```  
* compare the proof of (n-1) and n block proof to solve the puzzle and see if the hash is still under the defined target  
``` hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()```  
``` if hash_operation[:4] != '0000': ```  

The [endpoints/interfaces](https://github.com/Sarthak99/Python/blob/f98622e1be38546e80cc77894106311cb7f2af9f/Blockchain/blockchain.py#L91-L120) will work as below:  
* _/mine_block_ will let an user mine a new block.  
* _/get_chain_ will fetch the entire chain for display.  
* _/is_valid_ will verify if the entire chain, blocks and the cryptographical links are valid.
***  

### Create a crytpocurrency
To build a crypto, we need a minimal valid blockchain as an underlying implementation. Next we would create some transactions like sending tokens between different users. Each of these trx would come with some mining rewards in terms of the same crypto for the miner. The most important implementation of a crypto is to make it a [decentralized network](https://en.wikipedia.org/wiki/Decentralization) with P2P communications.  
An hypothetical cryptocurrency by the name "satocoins" has been demonstrated here. Also here I will illustrate how some of the tech elites such as Bill Gates, Elon Musk and Jeff Bezos would be transacting these crypto among themselves. The actual implementation can be found [here](https://github.com/Sarthak99/Python/blob/master/Blockchain/satocoins.py).  Apart from the above implemented blockchain, let'sgo through some of the extra fragments of the crypto.  
* [add_transaction(/add_transaction)](https://github.com/Sarthak99/Python/blob/0c0dc85b1a1501c4a838d732ce8cca660fdcb689/Blockchain/satocoins.py#L90-L98) method adds some transcations to the mempool. These are the transcations that need to be mined to the blockchain later to be confirmed as a completed trx. Transaction template is listed [here](https://github.com/Sarthak99/Python/blob/master/Blockchain/templates/transaction_template.json).  A transaction to be posted would look like this.   
``` 
 {  
  "sender":"Bill Gates",  
  "receiver":"Elon Musk",  
  "amount":10000  
 }  
```  
* [add_node(/connect_node)](https://github.com/Sarthak99/Python/blob/0c0dc85b1a1501c4a838d732ce8cca660fdcb689/Blockchain/satocoins.py#L100-L103) method is responsible for adding new users into the P2P network.[Node template.](https://github.com/Sarthak99/Python/blob/master/Blockchain/templates/nodes_template.json)  
```
{  
 "nodes":["http://127.0.70.1:5005",  
          "http://127.0.0.1:5006",  
          "http://127.0.0.1:5007"]  
}
```
* [replace_chain](https://github.com/Sarthak99/Python/blob/0c0dc85b1a1501c4a838d732ce8cca660fdcb689/Blockchain/satocoins.py#L105-L127) method is one of the most important one in the way that this implements the consensus protocol in the blockchain and helps maintain an integrity of the data among peers in the network by the basic rule of "longest valid" chain. This GET interface can be called at any point in time by the user to make sure that their chain are always up-to-date.  
* The endpoints/interfaces for crypto are as below:
  * [_/add_transaction_](https://github.com/Sarthak99/Python/blob/0c0dc85b1a1501c4a838d732ce8cca660fdcb689/Blockchain/satocoins.py#L167-L177) is a POST implentation that will add the transaction into the mempool. This would still need to be mined using _/mine_block_ to be confirmed as a data in the blockchain.
  * [_/connect_node_](https://github.com/Sarthak99/Python/blob/0c0dc85b1a1501c4a838d732ce8cca660fdcb689/Blockchain/satocoins.py#L194-L204) is a POST call to add new peers into the network.
  * [_/replace_chain_](https://github.com/Sarthak99/Python/blob/0c0dc85b1a1501c4a838d732ce8cca660fdcb689/Blockchain/satocoins.py#L206-L215) is a call to update the longest chain in the network.  
  
***Demonstration***  
To simulate this crypto implementation we need to create 3 copies of the code and run them in parallel. This would simulate as 3 different users of the network.  
Next we would be changing the below snippets to treat them as [different users](https://github.com/Sarthak99/Python/tree/master/Blockchain/DemoObjects).
* [running port](https://github.com/Sarthak99/Python/blob/0c0dc85b1a1501c4a838d732ce8cca660fdcb689/Blockchain/satocoins.py#L219) to something unqiue to indicate as a new node in the network.  
* [miner identity](https://github.com/Sarthak99/Python/blob/0c0dc85b1a1501c4a838d732ce8cca660fdcb689/Blockchain/satocoins.py#L149) to award tokens to the miner of a block.  
Once the above changes have been made, run the 3 python files in IDE or through command line. For ease of use and better visual, [POSTMAN](https://www.postman.com/) can be used for the APIs. The steps of running through the demo can be viewed [here](https://youtu.be/WD98XkiEYH0).
Steps:  
1. BG ==> calls (GET) /get_chain ==> returns a blockchain with only the genesis block.  
2. BG ==> calls (POST) /connect_node with data (excluding self node) ==> to add peers to it's own network.  
3. EM ==> calls (POST) /connect_node with data (excluding self node) ==> to add peers to it's own network.  
4. JB ==> calls (POST) /connect_node with data (excluding self node) ==> to add peers to it's own network.  
5. BG ==> calls (GET) /mine_block ==> to mine a new block with just a self trx.  
6. EM ==> calls (GET) /get_chain ==> returns still the old chain with genesis block.  
7. EM ==> calls (GET) /replace_chain ==> updates the chain to the new chain from BG.  
8. JB ==> calls (GET) /replace_chain ==> updates the chain to the new chain from BG.  
9. EM ==> calls (POST) /add_transaction ==> creates a trx from EM to JB for 10000 satocoins.  
10. EM ==> calls (GET) /mine_block ==> adds the trx and the mining reward to a latest block.  
11. JB ==> calls (GET) /replace_chain ==> updates the chain to the new chain from EM.  
12. JB ==> calls (POST) /add_transaction ==> creates a trx from JB to BG for 100000 satocoins.  
13. JB ==> calls (GET) /mine_block ==> adds the trx and the mining reward to a latest block.  
14. BG ==> calls (GET) /replace_chain ==> updates the chain to the new chain from JB.  
15. EM ==> calls (GET) /replace_chain ==> updates the chain to the new chain from JB.  

**!!_Documentation in progress_!!**   
<img src = "http://horticulture.tg.nic.in/img/work-in-progress-wip.jpg" width=220 height=200>
