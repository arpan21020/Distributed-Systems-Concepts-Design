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
from leaseTimer import ThreadTimer

globalfile = 0


# Define your RaftServer class implementing RaftClusterServicer
class RaftClusterServicer(raft_pb2_grpc.RaftClusterServicer):
    def __init__(self, ip, port, nodeLists):
        # Initialize your server state variables here
        self.leader_id = None
        self.leader_lease = ThreadTimer(0, self.fun)
        self.term = 0
        self.votedFor = None
        self.log = [[0, "key", "value"]]
        # [["term", "key", "value"], ["term", "key", "value"]]
        self.electionTimer = None
        self.data = {}
        self.ip = ip
        self.port = port
        self.state = 0
        self.commitIndex = 0
        self.electionTimeout = random.randrange(5, 10)
        self.heartbeatTime = 1
        self.prev = {}
        for node in nodeLists:
            if node != ip + ":" + port:
                self.prev[node] = 0

        self.lease_duration = 4
        self.nodeLists = nodeLists
        # self.lastlogIndex = 0
        # self.lastlogTerm = 0

    def fun(self):
        # print("Waiting for old leader lease to expire")
        return

    def restart_electionTimer(self):
        # Stop the existing timer if it is running
        if self.electionTimer.is_alive():
            self.electionTimer.cancel()

        # Create a new timer
        print("Election timer restarted at", self.ip, self.port)
        self.electionTimer = threading.Timer(self.electionTimeout, self.election)

        # Start the new timer
        self.electionTimer.start()

    def AppendEntry(self, request, context):
        if self.term <= request.term:
            self.term = request.term
            self.state = 0
            self.votedFor = None

        if self.term > request.term:
            return raft_pb2.AppendEntryReply(term=self.term, success=False)
        # if (request.prevLogIndex == 0):
        #     print()
        self.restart_electionTimer()
        self.leader_lease.update_leader_lease(request.leaseInterval)
        self.leader_id = request.leaderId
        # if (request.prevLogIndex < 0):

        try:
            if self.log[request.prevLogIndex][0] != request.prevLogTerm:
                print()
                print("Line 77", self.log[request.prevLogIndex][0], request.prevLogTerm)
                print()
                # print()
                # print("Append entries failed due to this")
                return raft_pb2.AppendEntryReply(term=self.term, success=False)
        except:
            # if request.prevLogIndex != -1:
            #     return raft_pb2.AppendEntryReply(term=self.term, success=False)
            # print(self.log)
            # print("HERE")
            # print(request.prevLogIndex)
            # print(self.log)
            # print(type(request.entries))
            # print("BEFORE\n")
            # print(self.log[request.prevLogIndex][0], request.prevLogTerm)
            # print("HERE")
            return raft_pb2.AppendEntryReply(term=self.term, success=False)

        # self.log=request.entries
        self.log = []
        for i in request.entries:
            self.data[i.key] = i.value
            self.log.append([i.term, i.key, i.value])

        print(f"AppendEntry to {self.ip}:{self.port } at term {self.term }")
        self.commitIndex = request.leaderCommit

        return raft_pb2.AppendEntryReply(term=self.term, success=True)

        # # Check if the log at prevLogIndex has the same term as prevLogTerm
        # if (
        #     len(self.log) <= request.prevLogIndex
        #     or self.log[request.prevLogIndex].term != request.prevLogTerm
        # ):
        #     return raft_pb2.AppendEntryReply(term=self.term, success=False)

        # # Remove any conflicting entries and append new entries
        # self.log = self.log[: request.prevLogIndex + 1] + list(request.entries)

        # # If leaderCommit > commitIndex, set commitIndex = min(leaderCommit, index of last new entry)
        # if request.leaderCommit > self.commitIndex:
        #     self.commitIndex = min(request.leaderCommit, len(self.log) - 1)

        # # else:
        # #     # Reject the request due to leader lease expiration or mismatch
        # #     return raft_pb2.AppendEntryReply(term=self.term, success=False)

    # Implement RequestVote RPC
    def RequestVote(self, request, context):
        print(f"Request vote received at {self.ip}:{self.port } at term {self.term}")

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
                term=self.term,
                success=True,
                oldLeaderLease=self.leader_lease.remaining(),
            )
        else:
            print(f"Response from {self.ip}:{self.port } at term {self.term}")

            # Deny vote if the request is invalid
            return raft_pb2.RequestVoteReply(
                term=self.term,
                success=False,
                oldLeaderLease=self.leader_lease.remaining(),
            )

    def sendHeartbeat(self):
        # Send heartbeat to all nodes
        print(f"HeartBeat sent from {self.ip}:{self.port } at term {self.term}")

        curr = self.ip + ":" + self.port
        entries_lst = []
        for i in self.log:

            entries_lst.append(raft_pb2.LogEntry(term=i[0], key=i[1], value=i[2]))
        maj = 1
        flag = 0
        maxresponse = 0
        for node in self.nodeLists:
            if node != curr:
                try:
                    channel = grpc.insecure_channel(node)
                    stub = raft_pb2_grpc.RaftClusterStub(channel)
                    response = stub.AppendEntry(
                        raft_pb2.AppendEntryRequest(
                            term=self.term,  # current term
                            leaderId=curr,  # current leader
                            prevLogIndex=max(
                                0, self.prev[node]
                            ),  # index of log entry immediately preceding new ones
                            prevLogTerm=self.log[self.prev[node]][
                                0
                            ],  # term of prevLogIndex entry
                            entries=entries_lst,  # contains all the log entries that have been recorded yet
                            leaderCommit=self.commitIndex,  # leader's commitIndex
                            leaseInterval=self.leader_lease.remaining(),  # leader's lease interval
                        )
                    )
                    # if response.success == False:
                    #     print("FALSE RETURNED")
                    if response.success:
                        # print(f"response.success from {node} is", response.success)
                        self.prev[node] = max(0, len(self.log) - 1)
                        # print(self.prev[node], ", line 197")
                        maj += 1
                        # self.restart_electionTimer()
                        # pass
                        # self.commitIndex = min(response.commitIndex, len(self.log) - 1)
                        # self.leader_lease.update_leader_lease(response.leaseInterval)
                    elif response.term > self.term:
                        flag = 1
                        maxresponse = max(maxresponse, response.term)
                    else:
                        self.prev[node] -= 1
                        self.prev[node] = max(0, self.prev[node])
                        # print(self.prev[node], ", line 208")
                        maj += 1
                        # self.restart_electionTimer()
                        # print("Heartbeat failed")
                except grpc.RpcError as rpc_error:
                    self.prev[node] = 0
                    # Handle gRPC errors
                    pass
        if flag == 1:
            self.state = 0
            self.term = maxresponse
            self.votedFor = None
            self.leader_id = None
            self.restart_electionTimer()
            return
        # print("maj, len(self.nodeLists) // 2", (maj, len(self.nodeLists) // 2))
        if maj > (len(self.nodeLists) // 2):
            print("Lease restarted after majority vote")
            self.leader_lease.restart()
            self.commitIndex = len(self.log) - 1
            # print(response)

    def election(self):
        # Start election
        # Record the start time
        start_time = time.time()
        self.state = 1
        print("Term inside Election: ", self.term)

        self.term += 1
        print(f"Election start at {self.ip}:{self.port } at term {self.term}")
        self.votedFor = self.ip + ":" + self.port
        self.votesReceived = 1
        # self.electionTimer = threading.Timer(self.electionTimeout, self.election)
        # self.electionTimer.start()
        # Send RequestVote RPC to all nodes
        max_old_lease = -1
        flag = 0
        for node in self.nodeLists:
            if node != self.ip + ":" + self.port:
                # print(type(node), "-", node)
                # print(type(self.ip), "-", self.ip)
                # print(type(self.port), "-", self.port)
                try:
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
                    if response.term > self.term:
                        flag = 1
                except grpc.RpcError as rpc_error:
                    self.prev[node] = 0
                    # Handle gRPC errors
                    pass
            else:
                print("Requested Vote to self")
        if flag == 1:
            self.state = 0
            self.term = response.term
            self.votedFor = None
            self.leader_id = None

            self.restart_electionTimer()

            return

        # Check if majority votes received
        if self.votesReceived > (len(self.nodeLists) // 2):
            # while (remaining_time(max_old_lease) > 0):
            max_old_lease_seconds = max_old_lease

            # Call self.fun
            # self.fun()

            # Wait until max_old_lease duration is elapsed
            while time.time() - start_time < max_old_lease_seconds:
                # print(time.time() - start_time)
                # print(max_old_lease_seconds)
                pass
            self.electionTimer.cancel()

            self.state = 2
            print(f"Leader elected {self.ip}:{self.port } at term {self.term }")
            self.leader_id = self.ip + ":" + self.port
            self.leader_lease = ThreadTimer(
                self.lease_duration, self.leader_lease.renew_leader_lease
            )
            self.leader_lease.start()
            # self.leader_lease.remaining() = time.time() + self.lease_duration

            while self.state == 2:
                if self.leader_lease.remaining() <= 0:
                    self.leader_id = None
                    self.state = 0
                    break
                self.sendHeartbeat()
                time.sleep(self.heartbeatTime)
            if self.state == 0:
                print("Leader stepped down")
                self.restart_electionTimer()
            else:  # impossible case
                print("Unexpected encounter at line 278 (impossible case)")
        else:
            self.votedFor = None
            self.restart_electionTimer()

    def ServeClient(self, request, context):
        if self.state == 2:
            req = request.Request.split(" ")
            if req[0] == "GET":
                print(
                    f"GET request received at {self.ip}:{self.port } at term {self.term }"
                )
                key = req[1]
                if key in self.data:
                    return raft_pb2.ServeClientReply(
                        Data=self.data[key], LeaderID=self.leader_id, Success=True
                    )
                else:

                    return raft_pb2.ServeClientReply(
                        Data="", LeaderID=self.leader_id, Success=True
                    )
            elif req[0] == "SET":
                print(
                    f"SET request received at {self.ip}:{self.port } at term {self.term }"
                )
                key = req[1]
                value = req[2]
                self.data[key] = value
                self.log.append([self.term, key, value])
                return raft_pb2.ServeClientReply(
                    Data="Key-Value pair added", LeaderID=self.leader_id, Success=True
                )
        else:
            if self.leader_id is not None:
                return raft_pb2.ServeClientReply(
                    Data="Node not a leader", LeaderID=self.leader_id, Success=False
                )

            else:
                return raft_pb2.ServeClientReply(
                    Data="Leader Not available", LeaderID="NULL", Success=False
                )

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
    # def renew_leader_lease(self):
    #     while True:
    #         # Update leader lease expiry time
    #         self.leader_lease.remaining() = time.time() + self.lease_duration


if __name__ == "__main__":
    # Define the list of nodes in the cluster
    # read command line arguments

    x = sys.argv[1:]
    i = int(x[0]) - 1
    globalfile = i
    # print(x)
    # print(type(x))
    try:
        nodeLists = [
            "localhost:50051",
            "localhost:50052",
            "localhost:50053",
            "localhost:50054",
            "localhost:50055",
        ]
        logging.basicConfig()
        f = nodeLists[i].split(":")
        node = RaftClusterServicer(f[0], f[1], nodeLists)
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=6))
        raft_pb2_grpc.add_RaftClusterServicer_to_server(node, server)
        server.add_insecure_port(nodeLists[i])
        server.start()
        print("Term:    ", node.term)
        node.electionTimer = threading.Timer(node.electionTimeout, node.election)
        node.electionTimer.start()
        # server.wait_for_termination()

        server.wait_for_termination()
    except KeyboardInterrupt:
        node.electionTimer.cancel()
        # if node.state == 0:
        #     print("Follower crashed at term", node.term)
        # elif node.state == 1:
        #     print("Candidate crashed at term", node.term)
        # else:
        #     print("Leader crashed at term", node.term)
        exit(1)
    except RuntimeError as e:
        # print("-----------------")
        # print(str(e))
        pass
        # print("-----------------")
