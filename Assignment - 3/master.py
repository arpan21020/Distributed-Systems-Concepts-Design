import random
import subprocess
from concurrent import futures
from time import sleep
import grpc
import kmeans_pb2
import kmeans_pb2_grpc
from math import *
import sys
import threading
import os


class Master:
    def __init__(self, m, r, k, max_iterations):
        self.num_mappers = m
        self.num_reducers = r
        self.num_centroids = k
        self.points = []
        self.centroids = []
        self.new_list = []
        # self.iterations = 0
        self.max_iterations = max_iterations
        portm = 50000
        portr = 60000
        self.mappers = []
        self.reducers = []
        self.successList = [False]*m
        for i in range(m):
            self.mappers.append("localhost:" + str(portm + i))
        for i in range(r):
            self.reducers.append("localhost:" + str(portr + i))
        # for i in range(self.num_centroids):
        with open("Data/Input/points.txt", "r") as f:
            points = f.readlines()
            for i in range(len(points)):
                point = points[i].split(",")
                self.points.append([float(point[0]), float(point[1])])

        # select k random points as initial centroids
        self.centroids = random.sample(self.points, self.num_centroids)
        print("Initial Centroids: ", self.centroids)

        for i in range(len(self.centroids)):
            self.new_list.append([0, 0])

        self.input_splits = self.divide_input_data()

    def centroid_compilation(self):
        with open("Data/centroids.txt", "w") as f:
            for i in self.centroids:
                f.write(str(i[0]) + "," + str(i[1]) + "\n")

    def InitiateMapReduce(self):
        # for i in range(self.max_iterations):
        for i in range(3):
            self.run_mapper()
            self.run_reducer()
            print(self.centroids)
            print(self.new_list)
            if i != 0 and self.convergence():
                print("Converged at iteration: ", i+1)
                break
            else:
                self.centroids = self.new_list
            self.centroid_compilation()
            # self
        # compile the output received from reducers

    def divide_input_data(self):
        m = self.num_mappers
        ll = len(self.points)
        pt = int(ll / m)
        l = []
        start = 0
        end = pt
        md = ll % m
        for i in range(m):
            if md > 0:
                end = end + 1
                md -= 1
            else:
                end = end
            l.append([start, end])
            start = end
            end = end + pt
        print("Mappers Division of Input Data: ", l)
        return l

    def call_mapper(self, id):
    
        try:
            node = self.mappers[id]
            channel = grpc.insecure_channel(node)  # mapper IP:port
            stub = kmeans_pb2_grpc.MapperStub(channel)
            cent = []
            for i in range(len(self.centroids)):
                cent.append(
                    kmeans_pb2.centroids(x=self.centroids[i][0], y=self.centroids[i][1])
                )
            response = stub.call_mapper(
                kmeans_pb2.InputSplitRequest(
                    startidx=self.input_splits[id][0],
                    endidx=self.input_splits[id][1],
                    centroidlist=cent,
                    mapper_id=id,
                    no_reducers=self.num_reducers,
                )
            )
            print(f"Response success value for {id}:", response.success)
            if response.success:
                print(id)
                self.successList[id] = True
        except KeyboardInterrupt:
            print("Failure in Mapper: ", id)

    def run_mapper(self):
        print("Final Centroids: ", self.centroids)
        threads = []
        for id in range(self.num_mappers):
            t = threading.Thread(target=self.call_mapper, args=(id,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
        # Spawn reducer process and pass necessary parameters
        # subprocess.run(["python", "reducer.py", i])

        # pass

    def call_reducer(self, id):
        print("CALLING REDUCER")
        try:
            node = self.reducers[id]
            channel = grpc.insecure_channel(node)  # reducer IP:port
            stub = kmeans_pb2_grpc.ReducerStub(channel)
            cent = []
            for i in range(len(self.centroids)):
                cent.append(
                    kmeans_pb2.centroids(x=self.centroids[i][0], y=self.centroids[i][1])
                )
            response = stub.call_reducer(
                kmeans_pb2.reducerinput(
                    reducer_id=id,
                    centroidlist=cent,
                    num_mappers=self.num_mappers,
                    mappers=self.mappers,
                )
            )
            read_output = response.reduce_output
            print("*"*40,"read output","*"*40)
            
            print(read_output)
            print("*"*40,"read output","*"*40)
            lst = read_output.split("\n")
            print(self.new_list,"nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn")
            for i in lst:
                if i:
                    temp = i.split(",")
                    print(temp,"-------------------"  )
                    self.new_list[int(temp[0])] = [float(temp[1]), float(temp[2])]
            # print(response.success)
        except KeyboardInterrupt:
            print("Failure in Reducer: ", id)

    def convergence(self):
        if len(self.centroids) != len(self.new_list):
            return False
        for i in range(len(self.centroids)):
            if round(self.centroids[i][0], 2) != round(self.new_list[i][0], 2) or round(self.centroids[i][1], 2) != round(self.new_list[i][1], 2):
                return False
        return True

    def run_reducer(self):
        if False in self.successList:
            return
        else:
            threads = []
            for id in range(self.num_reducers):
                t = threading.Thread(target=self.call_reducer, args=(id,))
                threads.append(t)
                t.start()

            for t in threads:
                t.join()

        # Spawn mapper process and pass necessary parameters
        # subprocess.run(["python", "mapper.py", input_split])
        # pass


def serve():
    # server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # kmeans_pb2_grpc.add_(Master(m, r, k), server)
    # server.add_insecure_port('[::]:50051')
    # server.start()
    # server.wait_for_termination()
    master = Master(m, r, k,max_iterations)
    master.InitiateMapReduce()


def run_python_file(file_name):
    command = f"start cmd /k python {file_name}"
    subprocess.run(command, shell=True)


if __name__ == "__main__":
    # m = sys.argv[1]
    # r = sys.argv[2]
    # k = sys.argv[3]
    
    # m = int(input("Enter the number of mappers: "))
    # r = int(input("Enter the number of reducers: "))
    # k = int(input("Enter the number of centroids: "))
    # max_iterations = int(input("Enter the maximum number of iterations: "))
    m = 2
    r = 2
    k = 6
    max_iterations = 20
    for id in range(m):
        run_python_file(f"mapper.py {50000+id}")
        
    for id in range(r):
        run_python_file(f"reducer.py {60000+id}")
    print("Master Node Started...")
    sleep(10)
    serve()
