#Groups will maintain a list of users who are currently part of the group. 
# Users can join or leave the group, and this information will be updated on the GROUP server.
#Groups will store messages sent by users. When a user requests messages from a group, the GROUP server will fetch the relevant messages and send them to the user.

#The GROUP server will store messages sent by users within each group. This includes the timestamp and the message content.

'''
    -maintain user list - update and delete
    -maintain user messages - update and retrieve
    -accept message if user is in userlist - sends SUCCESS otherwise FAILURE
    
'''

import zmq
import json
import sys
import threading
import time
from random import randint, random

def tprint(msg):
    """like print, but won't get newlines confused with multiple threads"""
    sys.stdout.write(msg + '\n')
    sys.stdout.flush()
  
  
class ServerTask(threading.Thread):
    """ServerTask"""
    def __init__(self,port,max_users):
        self.port=port
        self.max_users=max_users
        threading.Thread.__init__ (self)

    def run(self):
        context = zmq.Context()
        frontend = context.socket(zmq.ROUTER)
        frontend.bind(f'tcp://*:{self.port}')

        backend = context.socket(zmq.DEALER)
        backend.bind('inproc://backend')

        workers = []
        for i in range(self.max_users):
            worker = ServerWorker(context)
            worker.start()
            workers.append(worker)

        zmq.proxy(frontend, backend)

        frontend.close()
        backend.close()
        context.term()
class ServerWorker(threading.Thread):
    """ServerWorker"""
    def __init__(self, context):
        threading.Thread.__init__ (self)
        self.context = context

    def run(self):
        worker = self.context.socket(zmq.DEALER)
        worker.connect('inproc://backend')
        tprint('Worker started')
        while True:
            ident, msg = worker.recv_multipart()
            tprint('Worker received %s from %s' % (msg, ident))
            replies = randint(0,4)
            for i in range(replies):
                time.sleep(1. / (randint(1,10)))
                worker.send_multipart([ident, msg])

        worker.close()

  
class Group_Server:
    
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:5556")
        self.user_list={}
    