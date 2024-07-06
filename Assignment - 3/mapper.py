import random
import subprocess
from concurrent import futures
import grpc
import kmeans_pb2
import kmeans_pb2_grpc
from math import *
import logging
import sys
import os
import time

class Mapper(kmeans_pb2_grpc.MapperServicer):

    def __init__(self, port):
        self.start_index = -1
        self.end_index = -1
        self.centroids = []
        self.data = []
        self.output = []
        self.id = f"localhost:{port}"
        # self.map_no = -1
        self.num_reducers = 0
        self.MapperID = 0
        self.isProbabilisticFailure = False
        

        # print(self.data)

    def map(self):
        self.output = []
        # print("Centroids: ",self.centroids)
        
        # Process each data point in the input split
        for i in range(self.end_index-self.start_index):
            try:
                data_point = self.data[i]
            except Exception as e:
                print("Error:",e)
                print("i:",i)
                quit()
                break
            # Find the nearest centroid for the data point
            
            nearest_centroid = self.find_nearest_centroid(data_point)
            # print("Nearest Centroid: ",nearest_centroid)
            # Output the key-value pair
            # output = f"{nearest_centroid},{data_point[0]},{data_point[1]}"
            # Write the output to a file in the mapper's directory
            self.output.append({nearest_centroid: data_point})

            # if self.output.get(nearest_centroid) == None:
            #     self.output[nearest_centroid] = []
            # self.output[nearest_centroid].append(data_point)
        # print(self.output)
        # print("Output: ",self.output)
        return self.output

    def find_nearest_centroid(self, data_point):
        # Initialize variables
        nearest_centroid_index = None
        min_distance = float("inf")

        # Calculate the distance between the data point and each centroid
        for i, centroid in enumerate(self.centroids):
            distance = self.calculate_distance(data_point, centroid)
            

            # Update the nearest centroid if the distance is smaller
            if distance < min_distance:
                min_distance = distance
                nearest_centroid_index = i

        # Return the index of the nearest centroid
        return nearest_centroid_index

    def calculate_distance(self, point1, point2):
        distance = 0
        for i in range(len(point1)):
            distance += (point1[i] - point2[i]) ** 2
        distance = distance**0.5
        # print("distance:",distance)
        return distance

    def partition(self, num_reducers, map_out,append_flg):
        # partition mapper
        partitions = [[] for _ in range(num_reducers)]
        # print("Map_out: ",map_out,"---------------------------------------")
        for dict in map_out:
            # print("Dict: ",dict.items())
            for key, value in dict.items():
                partition_index = key % num_reducers
                # print("Partition Index: ",partition_index)
                # print("Key: ",key)
                # print('Value: ',value)
                # print("no of reducers: ",num_reducers)
                # print()
                partitions[partition_index].append((key, value))
        # for partition in partitions:
        #     print(partition)
        for i, partition in enumerate(partitions):
            if append_flg==False:
                print("Removing previous partition file")
                with open(
                    f"Data/Mappers/M{self.MapperID+1}/partition_{i+1}.txt", "w"
                ) as file:
                    for key, value in partition:
                        file.write(f"{key},{value[0]},{value[1]}\n")
            else:
                print("Appending to previous partition file")
                with open(
                    f"Data/Mappers/M{self.MapperID+1}/partition_{i+1}.txt", "a"
                ) as file:
                    for key, value in partition:
                        file.write(f"{key},{value[0]},{value[1]}\n")
            # with open(
            #     f"M{self.MapperID+1}_partition_{i+1}.txt", "a"
            # ) as file:
            #     for key, value in partition:
            #         file.write(f"{key},{value[0]},{value[1]}\n")
            # with open(
            #     f"M{self.MapperID+1}_partition_{i+1}.txt", "a"
            # ) as file:
            #     file.write("-------------------------------------------\n")
        # done

    def call_mapper(self, request, context):
        try:
            # print("*************************************Mapper called*********************************************")
            # Extract the input parameters
            self.start_index = request.startidx
            self.end_index = request.endidx
            cent = request.centroidlist
            append_flag = request.append
            self.isProbabilisticFailure = False

            # probabilistic function of mapper failure
            if ((request.mapper_id%2==0) and (random.random() < 0.5)):
                print("Mapper failed due to probabilistic failure")
                self.isProbabilisticFailure = True
                return kmeans_pb2.mapreturn(success=False)

            self.centroids = []
            for c in cent:
                self.centroids.append([c.x, c.y])
            self.MapperID = request.mapper_id
            self.num_reducers = request.no_reducers
            dir_path = f"Data/Mappers/M{request.mapper_id+1}"
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

            with open("Data/Input/points5.txt", "r") as file:
                points = file.readlines()
                self.data=[]
                for i in range(self.start_index, self.end_index):
                    point = points[i].split(",")
                    self.data.append([float(point[0]), float(point[1])])

            map_out = self.map()
            print(f"Mapper {self.MapperID+1} completed mapping")
            # time.sleep(6)
            self.partition(self.num_reducers, map_out,append_flag)
            print(f"Mapper {self.MapperID+1} completed partitioning")
            return kmeans_pb2.mapreturn(success=True)
        except KeyboardInterrupt:
            print("Failure in Mapper: ", self.MapperID)
            with open(f"Data/Mappers/M{self.MapperID+1}/partition_{i+1}.txt", "w") as file:
                file.write("")
            return kmeans_pb2.mapreturn(success=False)


    def GivereducerInput(self, request, context):
        if self.isProbabilisticFailure:
            return kmeans_pb2.ReducerOutput(success=False, map_outputs=[])
        requestID = request.reducer_id
        print(f"Reducer {requestID+1} requested Mapper {self.MapperID+1} for input")
        with open(
            f"Data/Mappers/M{self.MapperID+1}/partition_{requestID+1}.txt", "r"
        ) as file:
            r = file.readlines()

            l = []
            for i in r:
                #print("I: ",i)
                d = i.split(",")
                temp = kmeans_pb2.trio(
                    x=float(d[1]), y=float(d[2]), centroidId=int(d[0])
                )
                l.append(temp)
            # print("-------------------------------------------")
            print("Input has been sent to Reducer ", requestID+1)
            return kmeans_pb2.ReducerOutput(success=True, map_outputs=l)


def run(port):
    # Create a gRPC server
    logging.basicConfig()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    kmeans_pb2_grpc.add_MapperServicer_to_server(Mapper(port), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    port = sys.argv[1]
    obj = Mapper(port)
    print(f"Mapper Server:{port} started")
    run(port)
