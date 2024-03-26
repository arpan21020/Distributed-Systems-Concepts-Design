# 0- follower
# 1- candidate
# 2- leader

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


# Define your RaftServer class implementing RaftClusterServicer
class RaftClusterServicer(raft_pb2_grpc.RaftClusterServicer):
    def __init__(self, ip, port, nodeLists):
        # Initialize your server state variables here
        self.leader_id = None
        self.leader_lease_expiry = 10
        self.lease_duration = 10  # example lease duration in seconds
        self.term = 0
        self.votedFor = None
        self.log = []
        # log  = key: current term, value: data
        self.electionTimer = None
        self.data = {}
        self.ip = ip
        self.port = port
        self.state = 0
        self.commitIndex = 0
        self.electionTimeout = random.randrange(5, 10)
        self.heartbeatTime = 1

        self.lease_duration = 10
        self.nodeLists = nodeLists
        # self.lastlogIndex = 0
        # self.lastlogTerm = 0

    def restart_electionTimer(self):
        # Stop the existing timer if it is running
        if self.electionTimer.is_alive():
            self.electionTimer.cancel()

        # Create a new timer
        self.electionTimer = threading.Timer(self.electionTimeout, self.election)

        # Start the new timer
        self.electionTimer.start()

    # Implement AppendEntry RPC
    def AppendEntry(self, request, context):
        # if request
        # Handle AppendEntry logic here
        # Check leader lease validity
        # print("Lets go!!")
        if (
            self.leader_id == request.leaderId
            and self.leader_lease_expiry > time.time()
        ):
            # Process the AppendEntry request
            return raft_pb2.AppendEntryReply(term=1, success=True)
        else:
            # Reject the request due to leader lease expiration or mismatch
            return raft_pb2.AppendEntryReply(term=1, success=False)

    # Implement RequestVote RPC
    def RequestVote(self, request, context):
        if self.term < request.term:
            self.term = request.term
            self.state = 0
            self.votedFor = None

        lasterm = 0
        if len(self.log) > 0:
            lasterm = self.log[-1][0]
        logOk = (request.term > lasterm) or (
            request.lastLogTerm == lasterm and request.lastLogIndex + 1 >= len(self.log)
        )
        if (
            request.term == self.term
            and logOk
            and self.votedFor in [None, request.candidateId]
        ):
            # Grant vote if the request is valid
            self.votedFor = request.candidateId
            self.restart_electionTimer()
            return raft_pb2.RequestVoteReply(
                term=self.term, success=True, oldLeaderLease=self.leader_lease_expiry
            )
        else:
            # Deny vote if the request is invalid
            return raft_pb2.RequestVoteReply(
                term=self.term, success=False, oldLeaderLease=self.leader_lease_expiry
            )

    def sendHeartbeat(self):
        # Send heartbeat to all nodes
        curr = self.ip + ":" + self.port
        for node in self.nodeLists:
            if node != curr:
                channel = grpc.insecure_channel(node)
                stub = raft_pb2_grpc.RaftClusterStub(channel)
                entries_lst = []
                for i in self.data:
                    entries_lst.append(
                        raft_pb2.LogEntry(term=i[0], key=i[1], value=[2])
                    )
                response = stub.AppendEntry(
                    raft_pb2.AppendEntryRequest(
                        term=self.term,
                        leaderId=curr,
                        prevLogIndex=len(self.data) - 1,
                        prevLogTerm=self.data[-1][0],
                        entries=entries_lst,
                        leaderCommit=self.commitIndex,
                        leaseInterval=self.leader_lease_expiry,
                    )
                )
                print(response)

    def election(self):
        # Start election
        self.state = 1
        self.term += 1
        self.votedFor = self.ip + ":" + self.port
        self.votesReceived = 1
        self.electionStart = time.time()
        self.electionEnd = self.electionStart + self.electionTimeout
        electionTimer = threading.Timer(self.electionTimeout, self.election)
        electionTimer.start()
        # Send RequestVote RPC to all nodes
        max_old_lease = -1
        for node in self.nodeLists:
            if node != self.ip + ":" + self.port:
                channel = grpc.insecure_channel(node)
                stub = raft_pb2_grpc.RaftClusterStub(channel)
                response = stub.RequestVote(
                    raft_pb2.RequestVoteRequest(
                        term=self.term,
                        candidateId=self.ip + ":" + self.port,
                        lastLogIndex=len(self.log) - 1 if len(self.log) > 0 else 0,
                        lastLogTerm=self.log[-1][0] if len(self.log) > 0 else 0,
                    )
                )
                max_old_lease = max(response.oldLeaderLease, max_old_lease)
                if response.success:
                    self.votesReceived += 1

        # Check if majority votes received
        if self.votesReceived > len(self.nodeLists) // 2:
            # while (maxoldlease > time.time()):
            #
            electionTimer.cancel()
            self.state = 2
            self.leader_id = self.ip + ":" + self.port
            # self.leader_lease_expiry = time.time() + self.lease_duration
            while self.state == 2:
                sending = threading.Timer(self.heartbeatTime, self.sendHeartbeat)
                sending.start()
        else:
            self.state = 0

    # Function to start the server
    # def start(self):
    #     logging.basicConfig()
    #     server = grpc.server(futures.ThreadPoolExecutor(max_workers=6))
    #     raft_pb2_grpc.add_RaftClusterServicer_to_server(
    #         RaftClusterServicer("localhost", "50051", nodeLists), server
    #     )
    #     server.add_insecure_port("[::]:50051")
    #     server.start()
    #     electionTimer = threading.Timer(self.electionTimeout, self.election)
    #     electionTimer.start()
    #     server.wait_for_termination()

    # Function to renew leader lease periodically
    def renew_leader_lease(self):
        while True:
            # Update leader lease expiry time
            self.leader_lease_expiry = time.time() + self.lease_duration


if __name__ == "__main__":
    # Define the list of nodes in the cluster
    nodeLists = [
        "localhost:50052",
        "localhost:50051",
    ]
    logging.basicConfig()
    node = RaftClusterServicer("localhost", "50051", nodeLists)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=6))
    raft_pb2_grpc.add_RaftClusterServicer_to_server(node, server)
    server.add_insecure_port("[::]:50051")
    server.start()
    electionTimer = threading.Timer(node.electionTimeout, node.election)
    electionTimer.start()
    server.wait_for_termination()
