import grpc
from concurrent import futures
import logging
import raft_pb2
import raft_pb2_grpc
import threading
import time
import random
import threading
import sys
from leaseTimer import ThreadTimer


import signal
import sys

class Client:
    def __init__(self, ip, port, nodeLists):
        self.ip = ip
        self.port = port
        self.nodeLists = nodeLists
        self.leader = None

    def clientRequest(self, index):
        try:
            while True:
                # Input Format :
                #   SET key value
                #   GET key
                s = input("Enter your request :")
                req = s.split(" ")
                # SET name1 Jaggu
                # GET name1
                if self.leader is None:
                    node = self.nodeLists[index]
                else:
                    node = self.leader
                print("Leader is :", node)
                # node = self.nodeLists[0]
                channel = grpc.insecure_channel(node)
                stub = raft_pb2_grpc.RaftClusterStub(channel)
                response = stub.ServeClient(raft_pb2.ServeClientArgs(Request=s))
                if response.Success:
                    self.leader = node
                    if req[0] == "GET":
                        print("Response from GET request:", response.Data)
                    elif req[0] == "SET":
                        print("Response from SET request:", response.Data)
                else:
                    if response.LeaderID == "NULL":
                        print(response.Data)
                    else:
                        print(response.Data)
                        print("Leader is :", response.LeaderID)
                        self.leader = response.LeaderID
        except grpc.RpcError as rpc_error:
            self.leader = None
            print("Try on next node", (index + 1))
            if index + 1 < len(self.nodeLists):
                self.clientRequest(index + 1)
            if index + 1 == len(self.nodeLists):
                self.clientRequest(0)
        except KeyboardInterrupt:
            print("Exiting the client")
            sys.exit(1)
        except Exception as e:
            # print(e)
            # print("Exiting the client")
            sys.exit(1)


cli = Client(
    "localhost",
    50060,
    [
            "34.121.167.38:50051",
            "34.121.88.44:50052",
            "34.28.12.220:50053",
            "34.16.68.230:50054",
            "34.133.87.83:50055",
    ],
)

cli.clientRequest(0)
