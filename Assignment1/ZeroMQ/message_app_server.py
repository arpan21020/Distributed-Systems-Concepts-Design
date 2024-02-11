
# The server will maintain a list of groups identified by a unique identifier. It will store the IP addresses associated with each group to facilitate communication.

#Users can request the list of available groups from the server.
'''
    Group Server Request:
        - Send Join Request
        {
            type: join
            UUID:
            IP-Address:
            Port:
            
        }
        message_server prints: JOIN REQUEST FROM LOCALHOST:2000 [IP: PORT]
        Message Server prints: SUCCESS
    
    Client Request:
         {
            type: get_group_list
            UUID:
            IP-Address:
            Port:  
        }
        -Request list of group server
        message_server prints: GROUP LIST REQUEST FROM LOCALHOST:2000 [or UUID]
        Message Server returns group_list
        
    
'''

import zmq
import json

class Message_Server:
    
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:5555")
        self.group_list=[]
    def print_details(self):
        print("Socket is listenting on port 5555.......")
        
    def register_group(self,details):
        self.save_messages(details)
        print(f"JOIN REQUEST FROM {details['UUID']} {details['IP-Address']}:{details['Port']}")
        return 
        
    def fetch_group_list(self,details):
        self.load_messages()
        print(f"GROUP LIST REQUEST FROM {details['UUID']} {details['IP-Address']}:{details['Port']}")
        return self.group_list
    
    def save_messages(self,messages):
        self.group_list.append(messages)

    def load_messages(self):
        return self.group_list

if __name__ == "__main__":
    message_server = Message_Server()
    message_server.print_details()

    while True:
        
        message = message_server.socket.recv_json()
        
        if(message["type"]=="join"):
           message_server.register_group(message)
           message_server.socket.send_json({"status":"SUCCESS"})
           
        elif(message["type"]=="get_group_list"):
            message_server.fetch_group_list(message)
            message.server.socket.send_json({"status":"SUCCESS","grouplist":message_server.group_list})
        else:
            message_server.socket.send_json({"status":"INVALID REQUEST"})
        
            
       