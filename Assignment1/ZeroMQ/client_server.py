

# Join multiple groups simultaneously
# Leave group server
# Write message to group server
'''
    Request Group Server List from message_server
    {
            type: get_group_list
            UUID:
            IP-Address:
            Port:  
    } 
    Print:  ServerName1 - localhost:1234
            ServerName2 - localhost:1235
    Join/Leave Request from Group Server
    {
            type: join/leave
            UUID:
            IP-Address:
            Port:  
    }
     Send Message format
    {
        type: store_message
        UUID:
        message:
    }
    Receive Message format
    {
        type: get_messages
        UUID:
        Timestamp:  argument as a string in the format "YYYY-MM-DDTHH:MM:SS"
    }
    Print : |Time stamp     |   Message |  

'''
import zmq
import sys
import threading
import uuid
import json


class ClientTask(threading.Thread):
    """ClientTask"""
    def __init__(self, ip,uuid,message_server_ip,message_server_port):
        self.ip = ip
        self.uuid=uuid
        self.message_server_ip=message_server_ip
        self.message_server_port=message_server_port
        self.serverList=[]
        self.joinedServer=[]
        
        threading.Thread.__init__(self)
        
    def menu(self):
        print("=====================Menu=======================")
        print("1. Request Group Server List from message_server")
        print("2. Join Request from Group Server")
        print("3. Leave Request from Group Server")
        print("4. Send Message")
        print("5. Receive Message")
        print("6. View Joined Servers")
        print("7. Exit")
        print("================================================\n\n")
        
        user_input = int(input("Enter your choice: "))
        return user_input
    
    
    def getServerList(self):
        context2 = zmq.Context()
        socket2 = context2.socket(zmq.REQ)
        socket2.connect(f"tcp://{message_server_ip}:{message_server_port}")
        socket2.send_json({"type":"get_group_list","UUID":self.uuid,"IP-Address":self.ip})
        message2 = socket2.recv_json()
        self.serverList=message2['grouplist']
        self.showServerList("ACTIVE GROUP SERVER IN MESSAGE SERVER",self.serverList)
        
        socket2.close()
        context2.term()
    
    def showServerList(self,message,list):
        print(f"******************{message}******************")
        for i in range(len(list)):
            print(f"{i+1}. {list[i]['UUID']} - {list[i]['IP-Address']}:{list[i]['Port']}")
        print("***********************************************\n")
    
    def joinServer(self):
        choice=int(input("Select Server number :"))
        context = zmq.Context()
        socket = context.socket(zmq.DEALER)
        # identity = u'worker-%d' % self.id
        gs_ip=self.serverList[choice-1]['IP-Address']
        gs_port=self.serverList[choice-1]['Port']
        identity=self.uuid
        socket.identity = identity.encode('ascii')
        socket.connect(f'tcp://{gs_ip}:{gs_port}')
        # print(f'Client {self.ip} started on port {gs_port}')
        poll = zmq.Poller()
        poll.register(socket, zmq.POLLIN)
        socket.send_string(f"type;join,UUID;{self.uuid},IP-Address;{self.ip}")
        # for i in range(self.max_users):
        sockets = dict(poll.poll(1000))
        if socket in sockets:
            msg = socket.recv()
            response=msg.decode()
            if(response=="SUCCESS"):
                self.joinedServer.append(self.serverList[choice-1])
                print("JOIN STATUS : SUCCESS")
            else:
                print("JOIN STATUS : FAILURE")
                
        socket.close()
        context.term()
        
    def leaveServer(self):
        choice=int(input("Select Server number :"))
        context = zmq.Context()
        socket = context.socket(zmq.DEALER)
        # identity = u'worker-%d' % self.id
        gs_ip=self.joinedServer[choice-1]['IP-Address']
        gs_port=self.joinedServer[choice-1]['Port']
        identity=self.uuid
        socket.identity = identity.encode('ascii')
        socket.connect(f'tcp://{gs_ip}:{gs_port}')
        # print(f'Client {self.ip} started on port {gs_port}')
        poll = zmq.Poller()
        poll.register(socket, zmq.POLLIN)
        socket.send_string(f"type;leave,UUID;{self.uuid},IP-Address;{self.ip}")
        # for i in range(self.max_users):
        sockets = dict(poll.poll(1000))
        if socket in sockets:
            msg = socket.recv()
            response=msg.decode()
            if(response=="SUCCESS"):
                self.joinedServer.remove(self.joinedServer[choice-1])
                print("LEAVE STATUS : SUCCESS")
            else:
                print("LEAVE STATUS : FAILURE")
                
        socket.close()
        context.term()
    def send_message(self):
        choice=int(input("Select Server number  :"))
        message=input("Enter the message :")
        context = zmq.Context()
        socket = context.socket(zmq.DEALER)
        # identity = u'worker-%d' % self.id
        gs_ip=self.joinedServer[choice-1]['IP-Address']
        gs_port=self.joinedServer[choice-1]['Port']
        identity=self.uuid
        socket.identity = identity.encode('ascii')
        socket.connect(f'tcp://{gs_ip}:{gs_port}')
        print(f'Client {self.ip} started on port {gs_port}')
        poll = zmq.Poller()
        poll.register(socket, zmq.POLLIN)
        socket.send_string(f"type;store_message,UUID;{self.uuid},IP-Address;{self.ip},message;{message}")
        # for i in range(self.max_users):
        sockets = dict(poll.poll(1000))
        if socket in sockets:
            msg = socket.recv()
            response=msg.decode()
            if(response=="SUCCESS"):
                print("MESSAGE SENT STATUS : SUCCESS")
            else:
                print("MESSAGE SENT STATUS : FAILURE")
                
        socket.close()
        context.term()
        pass
    def print_messages(self,messages):
        if(len(messages)==0):
            print("NO MESSAGES TO DISPLAY")
            return
    # Calculate the maximum widths for timestamp and message
        max_timestamp_width = max(len(lst[1]) for lst in messages)
        max_message_width = max(len(lst[0]) for lst in messages)

        # Print the header with appropriate width
        print(f"={'=' * (max_timestamp_width + 2)}={'=' * (max(max_message_width,7) + 2)}=")
        print(f"| {'Time stamp':<{max_timestamp_width}} | {'Message':<{max_message_width}} |")
        print(f"={'=' * (max_timestamp_width + 2)}={'=' * (max(max_message_width,7) + 2)}=")

        # Print messages with appropriate width
        for lst in messages:
            timestamp = lst[1]
            message = lst[0]
            print(f"| {timestamp:<{max_timestamp_width}} | {message:<{max_message_width}} |")
        print(f"={'=' * (max_timestamp_width + 2)}={'=' * (max(max_message_width,7) + 2)}=")
        print("\n")

    def fetch_messages(self):
        choice=int(input("Select Server number  :"))
        timestamp=input("Enter the timestamp(YYYY-MM-DDTHH:MM:SS) :")
        context = zmq.Context()
        socket = context.socket(zmq.DEALER)
        # identity = u'worker-%d' % self.id
        gs_ip=self.joinedServer[choice-1]['IP-Address']
        gs_port=self.joinedServer[choice-1]['Port']
        identity=self.uuid
        socket.identity = identity.encode('ascii')
        socket.connect(f'tcp://{gs_ip}:{gs_port}')
        poll = zmq.Poller()
        poll.register(socket, zmq.POLLIN)
        if(len(timestamp)==0):
            socket.send_string(f"type;get_messages,UUID;{self.uuid},IP-Address;{self.ip}")
        else:
            socket.send_string(f"type;get_messages,UUID;{self.uuid},IP-Address;{self.ip},timestamp;{timestamp}")
        # for i in range(self.max_users):
        sockets = dict(poll.poll(1000))
        if socket in sockets:
            msg = socket.recv()
            response=msg.decode()
            self.print_messages(json.loads(response))
            # if(response=="SUCCESS"):
            #     print("MESSAGES FETCHED STATUS : SUCCESS")
            # else:
            #     print("MESSAGES FETCHED STATUS : FAILURE")
                
        socket.close()
        context.term()
        pass
    def run(self):
        
        reqs = 0
        while True:
            user_input=self.menu()
            if(user_input==1):
               self.getServerList()
               continue
            elif(user_input==2):
                self.showServerList("\nENTER SERVER NUMBER TO JOIN",self.serverList)  
                self.joinServer()     
            elif(user_input==3):
                self.showServerList("\nENTER SERVER NUMBER TO LEAVE",self.joinedServer)
                self.leaveServer()   
                pass
            elif(user_input==4):
                self.showServerList("\nENTER SERVER NUMBER TO SEND MESSAGE",self.joinedServer)  
            
                self.send_message()
                
            elif(user_input==5):
                self.showServerList("\nENTER SERVER NUMBER TO FTECH MESSAGE",self.joinedServer)  
                
                self.fetch_messages()
                
            elif(user_input==6):
                self.showServerList("Joined Servers",self.joinedServer)
                
            elif(user_input==7):
                break
            
            

        

def main(ip,message_server_ip,message_server_port):
    # port1 = input("Enter the port number for server 1: ")
    # port2 = input("Enter the port number for server 2: ")
    
    # port2=5573
    uid=str(uuid.uuid4())
    
    user=ClientTask(ip,uid,message_server_ip,message_server_port)
    user.start()
    user.join()

if __name__ == "__main__":
    ip=sys.argv[1]
    message_server_ip=sys.argv[2]
    message_server_port=sys.argv[3]
    main(ip,message_server_ip,message_server_port)
