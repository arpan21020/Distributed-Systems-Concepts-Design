
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
        Group prints: JOIN REQUEST FROM 987a515c-a6e5-11ed-906b-76aef1e817c5 [UUID OF USER]
        
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
        if(details in self.group_list):
            return False
        self.save_messages(details)
        print(f"JOIN REQUEST FROM {details['UUID']} {details['IP-Address']}:{details['Port']}")
        return True 
        
    def fetch_group_list(self,details):
        self.load_messages()
        print(f"GROUP LIST REQUEST FROM {details['IP-Address']}:{details['UUID']}")
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
           ret=message_server.register_group(message)
           if(ret==False):
               message_server.socket.send_json({"status":"FAILURE"})
           message_server.socket.send_json({"status":"SUCCESS"})
           
        elif(message["type"]=="get_group_list"):
            message_server.fetch_group_list(message)
            message_server.socket.send_json({"status":"SUCCESS","grouplist":message_server.group_list})
        else:
            message_server.socket.send_json({"status":"INVALID REQUEST"})
        
            