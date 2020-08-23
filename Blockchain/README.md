**Welcome to the Blockchain project !!**  
This project has the basic components of [building a blockchain](https://github.com/Sarthak99/Python/blob/master/Blockchain/blockchain.py)  in python, creating an [hypothetical cryptocurrency](https://github.com/Sarthak99/Python/blob/master/Blockchain/satocoins.py) and [smart contracts]() in a blockchain.


### Build a basic blockchain
Below are some the code fragments to demonstrate the implementation of few important parts. The entire blockchain has been implemented in python and the interfacing has been done by flask framework.  
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

**!!_Documentation in progress_!!**   
<img src = "http://horticulture.tg.nic.in/img/work-in-progress-wip.jpg" width=220 height=200>
