from hashlib import sha256
import json
from datetime import datetime

class TX :
     def __init__(self, from_address, to_address, amount):
         self.from_address = from_address
         self.to_address = to_address 


class Block:
    def __init__(self ,timestamp, txs, previous_hash):
        
        self.timestamp = timestamp
        self.txs = txs
        self.previous_hash = previous_hash
        self.hash=self.calculate_hash()
        self.nonce = 0
        
    def calculate_hash(self):
        to_be_hashed = self.timestamp + str(self.txs) + self.previous_hash
        return sha256((to_be_hashed).encode()).hexdigest()

    def mine_block(self, difficulty):
        while (self.hash[0:difficulty] != "0" * difficulty):
          self.nonce += 1
          self.hash = self.calculate_hash()

        print("Total Trials:", self.nonce)
        print("Block mined:", self.hash)


class Blockchain:
    def __init__(self, difficulty, mining_reward):
      self.chain = [self.create_genesis_block()]
      self.difficulty = difficulty  # our hash must start with 4 zeros
      self.pending_txs =[]
      self.mining_reward = mining_reward

    def create_genesis_block(self):
      current_time = datetime.now().strftime("%H:%M:%S-%d-%b-%Y")
      return Block( current_time, [])

    def create_tx(self, tx):
      self.pending_txs.append(tx)
   

    def mine_pending_txs(self, miner_address):
      current_time = datetime.now().strftime("%H:%M:%S-%d-%b-%Y")
      new_block = Block(current_time, self.pending_txs)
      new_block.previous_hash = self.get_last_block().hash
      new_block.mine_block(self.difficulty)
      self.chain.append(new_block)
      # send reward to miner (when next tx is mined)
      self.pending_txs = [TX(None, miner_address, self.mining_reward)]

      
    def add_block(self, new_block):
      new_block.previous_hash = self.get_last_block().hash
      new_block.mine_block(self.difficulty)
      self.chain.append(new_block)

    def get_last_block(self):
      return self.chain[-1]

    def print_blocks(self):
      for block in self.chain:
        block.txs = {i + 1: tx.__dict__  for i,tx in enumerate(block.txs)}
        print(json.dumps(eval(str(block.__dict__)), indent=2))

    def get_balance(self, address):

      balance=0
      for block in self.chain:
        for tx in block.txs
          if address == tx.from_address:
            balance -= tx.amount
          if address == tx.to_address:
            balance += tx.amount
      return balance

    def is_chain_valid(self):
      for i in range(0, len(self.chain) - 1):
        curr_block = self.chain[i]
        next_block = self.chain[i + 1]
        if (curr_block.hash != curr_block.calculate_hash()  # 1st cond.
            or next_block.previous_hash != curr_block.hash):  # 2nd cond.
          return False

          return True  # if for-loop finishes and all conditions hold
    
circle_coding_coin = Blockchain(5,33)

address1="jvgdhfl"
address2="kdhxhfk"
miner_address="iehgsbv"

circle_coding_coin.create_tx(TX(address2, address1,10))
circle_coding_coin.create_tx(TX(address2, address1,5))

print("MIner is mining...")
circle_coding_coin.mine_pending_txs("miner")

circle_coding_coin.print_blocks
