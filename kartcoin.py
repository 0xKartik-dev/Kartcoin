#Module 2 , creating the crypto currency

#pip install Flask==0.12.2
#postman
#pip install requests==2.18.4
import datetime
import hashlib
import json
from flask import Flask,jsonify,request
import requests
from uuid.parse import uuid4
from urllib.parse import urlparse

#Part 1 - Building BlockChain
class Blockchain:
    def __init__(self):
        self.chain=[]
        self.transactions=[]
        self.create_block(proof =1,previous_hash='0')
        self.nodes = set()
        
    def create_block(self,proof,previous_hash):
        block= {'index': len(self.chain)+1,
                'timestamp': str(datetime.datetime.now()),
                'proof':proof,
                'previous_hash':previous_hash,
                'transactions': self.transactions}
        self.transactions = []
        self.chain.append(block)
        return block
    
    
# for getting previous block we just need to use the self block , wow ! superb!
    def get_previous_block(self):
        return self.chain[-1]
#end of previous_block fectch


# to do proof of work and set to set the hash to 0000 leading zeros    
    def proof_of_work(self,previous_proof):
        new_proof=1;
        check_proof=False
        while check_proof is False:
            hash_operation= hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] =='0000':
                check_proof=True
            else:
                new_proof+=1
        return new_proof


#to get a block, encode it and convert it to hexdigest   
    def hash(self,block):
        encoded_block= json.dumps(block,sort_keys= True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

#checking whether the previous hash of the current block is equal to hash of the previous block
#hash operation on the current block prrof and previous block proof, if the hash operation is equal to 
#0000 then block is good and update the previous block with the current block and increment the current block index to 1

    def is_chain_valid(self,chain):
        previous_block= chain[0]
        block_index=1
        while block_index<len(chain):
            block= chain[block_index]
            if block['previos_hash']!= self.hash(previous_block):
                return False
            previous_proof=previous_block['proof']
            proof = block['proof']
            hash_operation= hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block=block
            block_index +=1
        return True
    
    
    def add_transaction(self,sender,reciever,amount):
        self.transactions.append({'sender':sender,
                                  'reciever':reciever,
                                  'amount':amount})
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1
    
    def add_node(self,address):
        parsed_url = urlparse(address)
        self.add_node.add(parsed_url.netloc)
    
    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response= requests.get('http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length> max_length and self.is_chain_valid(chain):
                    max_length=length
                    longest_chain= chain
            if longest_chain:
                self.chain=longest_chain
                return True
            return False
            
            
            
            
#Part 2
#Minig our blockchain


#Creatting the web app
app = Flask(__name__)


#creating a node address for the node 5000
node_address = str(uuid4()).replace('-','')

#Creating the blockchain
blockchain = Blockchain()


#Minig a new block
@app.route('/mine_block',methods=['GET'])
def mine_block():
    previous_block=blockchain.get_previous_block()
    previous_proof=previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash=blockchain.hash(previous_block)
    blockchain.add_transaction(sender=node_address,reciever='kartik',amount=1)
    block= blockchain.create_block(proof,previous_hash)
    response = {'message':'congo ,you have mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof':block['proof'],
                'previous_hash':block['previous_hash'],
                'transactions':block['transactions']}
    return jsonify(response), 200

#Getting the full blockchain
@app.route('/get_chain',methods=['GET'])
def get_chain():
    response = {'chain':blockchain.chain,
                'length':len(blockchain.chain)}
    return jsonify(response), 200

#checking if the blockchain is valid or not
@app.route('/is_valid',methods=['GET'])
def is_valid():
    is_valid=blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response= {'message': 'All goood. Blockchain is valid'}
    else:
        response= {'message':'kartik we hava problem, Blockchain is not valid'}
    return jsonify(response),200


#Adding new Transaction to the blockchain using POST request
@app.route('/add_transaction',methods=['POST'])
def add_transaction():
    json=request.get_json()
    tranaction_keys=['sender','reciever','amount']
    if not all (key in json for key in tranaction_keys):
        return 'Some elementsof the transaction is missing!',400
    index = blockchain.add_transaction(json['sender'],json['reciever'],json['amount'])
    response = {'message': f'This transaction has been added to Block {index}' }
    return jsonify(response),201
    
    


#Part 3 Decentralizing the Blockchain

#Connecting new nodes
@app.route('/connect_node',methods=['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return "No Node ",400
    for node in nodes :
        blockchain.add_node(node)
    response =  {'message':'All the nodes are now connected ! The Kartcoin Blockchain now contains the :',
                 'total_nodes':list(blockchain.nodes)}
    return jsonify(response),201

#Replacing the chain by the longest chain if needed
@app.route('/replace_chain',methods=['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response= {'message': 'The Nodes had the longest chain and the Chaiun is Replaced by the Longest Chain',
                   'new_chain':blockchain.chain}
    else:
        response= {'message':'All good!,the Chain is the longest one.',
                   'actual_chain':blockchain.chain}
    return jsonify(response),200




#Running the app
app.run(host = '0.0.0.0' , port = 5000)


































            
    

        
    
        
        

