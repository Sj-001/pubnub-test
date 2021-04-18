import redis
import json
import time
import pickle
# from app_src.config import NEW_NODE_MSG

r = redis.Redis(host='localhost', port=6379, db=0)

CHANNELS = ['MESSAGE', 'BLOCK', 'BLOCKCHAIN', 'TRANSACTION', 'TXPOOL']


class PubSub:

    def __init__(self):
        # self.lastBlock = chainBlock
        # self.txPool = txPool
        self.messages = []
        self.publisher = r
        self.subscriber = r.pubsub()
        self.subscribeToChannels()
        self.thread = self.subscriber.run_in_thread(sleep_time=0.001)
        # self.broadcastMessage(NEW_NODE_MSG)

    def subscribeToChannels(self):
        for channel in CHANNELS:
            self.subscribe(channel)
        return True

    def subscribe(self, channel):
        self.subscriber.subscribe(**{channel: self.handleMessage})

    def handleMessage(self, message):
        if message:
            channel = message['channel']
            data = message['data']
            parsedMessage = pickle.loads(data)
            if channel == b'MESSAGE':
                print("Handling new node...")
                print(parsedMessage)
                self.messages.append(parsedMessage)
                print('Added message.')
                # if parsedMessage == NEW_NODE_MSG:
                #     print("Broadcasting Chain...")
                #     self.broadcastChain()
                    # TODO self.broadcastTxPool()
            # if channel == b'BLOCK':
            #     print(parsedMessage)
            #     block = parsedMessage
            #     new_block = Block(block['timestamp'], block['data'], block['nonce'], block['difficulty'], block['reward'], block['hash'], block['miner'], block['previousHash'])
            #     self.lastBlock.addBlock(new_block)
            # if channel == b'BLOCKCHAIN':
            #     print(parsedMessage)
            #     if parsedMessage != self.lastBlock:
            #         if self.lastBlock and hasattr(parsedMessage, 'previousHash'):
            #             if parsedMessage.previousHash == self.lastBlock.hash:
            #                 self.lastBlock.addBlock(parsedMessage)                    
            #         else:
            #             self.lastBlock = self.lastBlock.replaceChain(parsedMessage) 
            #             #TODO self.txPool.clearBlockchainTransactions()
            #     pass
            # #TODO
            # if channel == b'TRANSACTION':
            #     print(parsedMessage)
            #     self.txPool.setTransaction(parsedMessage)
            # if channel == 'TXPOOL':
            #     self.txPool.setMap(parsedMessage)


    def unsubscribeChannel(self, channel, message=None, _callback=None):
        self.subscriber.unsubscribe(channel)
        if _callback and message:
            _callback(channel, message, self.subscribe)

    def publish(self, channel, message, _callback=None):
        pickledMessage = pickle.dumps(message)
        self.publisher.publish(channel, pickledMessage)
        if _callback:
            _callback(channel)
        return True

    def broadcastMessage(self, message):
        self.unsubscribeChannel('MESSAGE', message, self.publish)
        return True

    # def broadcastBlock(self, block):
    #     placeholder = block.previousBlock
    #     block.previousBlock = None
    #     self.publish('BLOCK', block)
    #     block.previousBlock = placeholder

    # def broadcastChain(self):
    #     self.unsubscribeChannel('BLOCKCHAIN', self.lastBlock, self.publish)
    #     return True
        

    # def broadcastTx(self, tx):
    #     self.unsubscribeChannel('TRANSACTION', transaction, self.publish)
        
    # def broadcastTxPool(self):
    #     self.unsubscribeChannel('TXPOOL', self.txPool, self.publish)

