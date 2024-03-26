#Groups will maintain a list of users who are currently part of the group. 
# Users can join or leave the group, and this information will be updated on the GROUP server.
#Groups will store messages sent by users. When a user requests messages from a group, the GROUP server will fetch the relevant messages and send them to the user.

#The GROUP server will store messages sent by users within each group. This includes the timestamp and the message content.

'''
    -maintain user list - update and delete
    -maintain user messages - update and retrieve
    -accept message if user is in userlist - sends SUCCESS otherwise FAILURE
    
    User Join/Leave Request format
        {
            type: join/leave
            UUID:
            IP-Address:
            Port:  
        }
    User Send Message format - also store the received time
    {
        type: store_message
        UUID:
        Ip-Address:
        message:
    }
    Group prints: MESSAGE SEND FROM 987a515c-a6e5-11ed-906b-76aef1e817c5
    
    
    User Receive Message format
    {
        type: get_messages
        UUID:
        IP-Address:
        timestamp:
    }
    Group prints: MESSAGE REQUEST FROM 987a515c-a6e5-11ed-906b-76aef1e817c5 [UUID OF USER]
    
'''

import zmq
import json
import sys
import threading
import time
import uuid
import datetime
from random import randint, random
  
  
class ServerTask(threading.Thread):
    """ServerTask"""
    def __init__(self,port,ip,max_users):
        self.port=port
        self.ip=ip
        self.max_users=1
        threading.Thread.__init__ (self)
        

    def run(self):
        context = zmq.Context()
        frontend = context.socket(zmq.ROUTER)
        frontend.bind(f"tcp://0.0.0.0:{self.port}")
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
        self.user_list={}
        self.user_messages={}
        threading.Thread.__init__ (self)
        self.context = context

    def join_request(self,requested):
        self.user_list[requested['UUID']]={"IP-Address":requested['IP-Address']}
        print(f"JOIN REQUEST FROM {requested['IP-Address']}:{requested['UUID']} ")
        return
    def leave_request(self,requested):        
        self.user_list.pop(requested['UUID'])
        print(f"LEAVE REQUEST FROM {requested['IP-Address']}:{requested['UUID']}")
        return
    def save_message(self, requested):
        if requested['UUID'] not in self.user_list.keys():
            return False
        if requested['UUID'] not in self.user_messages.keys():
            self.user_messages[requested['UUID']] = []

        # Get the current timestamp
        timestamp = datetime.datetime.now().isoformat()

        # Append the message and timestamp as a tuple
        self.user_messages[requested['UUID']].append((requested['message'], timestamp))
        return True
    def get_messages(self, user_id, since=None):
        if user_id not in self.user_list or user_id not in self.user_messages:
            return None # User not found or no messages for the user

        if since is None:
            return self.user_messages[user_id]  # Return all messages if no date is mentioned

        # Convert the since parameter to a datetime object
        try:
            since_date = datetime.datetime.strptime(since, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            return []  # Invalid date format

        # Filter messages based on the specified date and time
        filtered_messages = [(message, timestamp) for message, timestamp in self.user_messages[user_id] 
                            if datetime.datetime.fromisoformat(timestamp) >= since_date]

        return filtered_messages
    def run(self):
        worker = self.context.socket(zmq.DEALER)
        worker.connect('inproc://backend')
        while True:
            # print("userlist:",self.user_list)
            ident, msg = worker.recv_multipart()
            request_dict=msg.decode('utf-8').split(',')
            requested={}
            for i in request_dict:
                key,value=i.split(';')
                requested[key]=value
            # print(requested)
            if(requested['type']=="join"):
                self.join_request(requested)
                worker.send_multipart([ident,b"SUCCESS"])
                
            elif(requested['type']=="leave"):
                self.leave_request(requested)
                worker.send_multipart([ident,b"SUCCESS"])  
            elif(requested['type']=="store_message"):
                if(self.save_message(requested)):
                    worker.send_multipart([ident,b"SUCCESS"])
                    print(f"MESSAGE SEND FROM {requested['UUID']}")
                else:
                    worker.send_multipart([ident,b"FAILURE"])
                
            elif(requested['type']=="get_messages"):
                print(f"Group prints: MESSAGE REQUEST FROM {requested['IP-Address']}:{requested['UUID']} ")
                if('timestamp' in requested.keys()):
                    msgs=self.get_messages(requested['UUID'], requested['timestamp'])
                else:
                    msgs=self.get_messages(requested['UUID'])
                if(msgs==None):
                    worker.send_multipart([ident,b"FAILURE"])
                else:
                    worker.send_multipart([ident,json.dumps(msgs).encode('utf-8')])
            else:
                print(f"Invalid Request from {msg}")
            # if len(msg)>0 and msg[0]=='exit':
            #     break
            replies = randint(0,4)
            for i in range(replies):
                pass
                # worker.send_multipart([ident, msg])
            
                # time.sleep(1. / (randint(1,10)))

        worker.close()

  
class Group_Server:
    
    def __init__(self,port,ip,server_id,server_port):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(f"tcp://{server_id}:{server_port}")
        self.id=str(uuid.uuid4())
        self.port=port
        self.ip=ip
    def isResistered(self):
        self.socket.send_json({"type":"join","UUID":self.id,"IP-Address":self.ip,"Port":self.port})
        response = self.socket.recv_json()
        if(response["status"]=="SUCCESS"):
            return True
        else:
            return False
def main(groupserver_port,groupserver_ip,messageserver_ip,messageserver_port):
    print(groupserver_port,groupserver_ip,messageserver_ip,messageserver_port)
    obj=Group_Server(groupserver_port,groupserver_ip,messageserver_ip,messageserver_port)
    status=obj.isResistered()
    print("Registeration status : SUCCESS")

    while(status):
        print("Server listening at port",obj.port,".........")
        groupserver = ServerTask(obj.port,obj.ip,max_users=1)
        groupserver.start()
        groupserver.join()


if __name__ == "__main__":
    groupserver_ip=sys.argv[1]
    groupserver_port=sys.argv[2]
    
    messageserver_ip=sys.argv[3]
    messageserver_port=sys.argv[4]

    
    main(groupserver_port,groupserver_ip,messageserver_ip,messageserver_port)
    
    