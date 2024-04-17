import os
import subprocess
from concurrent import futures
import grpc
import kmeans_pb2
import kmeans_pb2_grpc
from math import *
import math
import sys


class Reducer(kmeans_pb2_grpc.ReducerServicer):
    def __init__(self, port):
        self.key_values = {}
        self.id = f"localhost:{port}"
        self.reducer_id = -1  # reducer's ID
        self.centroids = []
        self.num_mappers = 0
        self.mappers = []
        self.output = 0

    def shuffle_and_sort(self, partitonedList):
        # sorting patitionedList on the basis of the third element
        partitonedList.sort(key=lambda x: x[2])
        dictionary = {}
        for inner_list in partitonedList:
            key = inner_list[2]  # Third element as key
            value = (inner_list[0], inner_list[1])  # Tuple of first and second elements
            if key in dictionary:
                dictionary[key].append(value)
            else:
                dictionary[key] = [value]

        self.output = dictionary

    def reduce(self, centroidId, list_points):
        # l = self.output[centroidId]
        x = [i[0] for i in list_points]
        y = [i[1] for i in list_points]
        x = sum(x) / len(x)
        y = sum(y) / len(y)

        with open(f"Data/Reducers/R{self.reducer_id+1}.txt", "a") as f:
            f.write(f"{centroidId},{x},{y}\n")
        # with open(f"R{self.reducer_id+1}.txt", "a") as f:
        #     f.write(f"{centroidId},{x},{y}\n")
        return centroidId, (x, y)

    def call_reducer(self, request, context):
        try:
            self.reducer_id = request.reducer_id
            self.num_mappers = request.num_mappers
            cent = request.centroidlist
            self.mappers = request.mappers
            with open(f"Data/Reducers/R{self.reducer_id+1}.txt", "w") as f:
                f.write("")
            # with open(f"R{self.reducer_id+1}.txt", "a") as f:
            #     f.write("-------------------------------------------\n")
            l = []
            for c in cent:
                l.append([c.x, c.y])
            self.centroids = l
            trio_list = []
            for id in self.mappers:
                try:
                    channel = grpc.insecure_channel(id)  # mapper IP:port
                    stub = kmeans_pb2_grpc.MapperStub(channel)
                    response = stub.GivereducerInput(
                        kmeans_pb2.ReducerInputRequest(reducer_id=self.reducer_id)
                    )
                    if response.success == True:
                        temp = response.map_outputs
                        # print("TEMP", temp)
                        for t in temp:
                            trio_list.append([t.x, t.y, t.centroidId])
                # print("TRIO LIST", trio_list)
                except:
                    continue
            self.shuffle_and_sort(trio_list)
            # print("TRIO---------------")
            # print(trio_list)
            for c, v in self.output.items():
                # print("c:", c, "v: ", v)
                self.reduce(c, v)
            file_read = open(f"Data/Reducers/R{self.reducer_id+1}.txt", "r")
            str1 = file_read.read()
            # self.reduce()
            file_read.close()
            return kmeans_pb2.Reducereturn(success=True, reduce_output=str1)
        except KeyboardInterrupt:
            print(f"Failure in Reducer: {self.reducer_id}")
            return kmeans_pb2.Reducereturn(success=False, reduce_output="Failure")

def run(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    kmeans_pb2_grpc.add_ReducerServicer_to_server(Reducer(port), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    port = sys.argv[1]
    obj = Reducer(port)
    print(f"Reducer Server:{port} started")

    run(port)
