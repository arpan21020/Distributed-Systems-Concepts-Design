import grpc
from concurrent import futures
import time
import uuid
import logging

# from shopping_pb2 import (
#     SearchItemRequest,
#     BuyItemRequest,
#     AddToWishListRequest,
#     RateItemRequest,
#     NotifyClientRequest,
#     NotifyClientResponse,
# )
# from shopping_pb2_grpc import (
#     MarketStub,
#     NotifyClientStub,
#     NotifyClientServicer,
#     add_NotifyClientServicer_to_server,
# )

import shopping_pb2
import shopping_pb2_grpc


class NotificationServicer(shopping_pb2_grpc.NotificationServicer):
    def NotifyClient(self, request, context):
        print("Buyer prints:")
        print(request.message)
        return shopping_pb2.NotifyClientResponse(
            result=shopping_pb2.NotifyClientResponse.SUCCESS
        )


# class NotifyClientServicerImpl(NotifyClientServicer):
#     def NotifyClient(self, request, context):
#         print("Buyer prints:")
#         print(request.message)
#         return NotifyClientResponse(result=NotifyClientResponse.SUCCESS)


def search_item(stub, item_name, category):
    request = shopping_pb2.SearchRequest(name=item_name, category=category)
    response = stub.SearchItem(request)
    print("Buyer prints:")
    for item in response.items:
        print(
            f"\nItem ID: {item.id}, Price: ${item.price}, Name: {item.name}, "
            f"Category: {item.category}\nDescription: {item.description}\n"
            f"Quantity Remaining: {item.quantity}\nRating: {item.rating} "
        )


def buy_item(stub, item_id, quantity, buyer_address):
    request = shopping_pb2.BuyRequest(
        id=item_id, quantity=quantity, buyer_address=buyer_address
    )
    response = stub.BuyItem(request)
    print("Buyer prints:")
    if response.result == response.SUCCESS:
        print("SUCCESS")
    else:
        print("FAIL")


def add_to_wishlist(stub, item_id, buyer_address):
    request = shopping_pb2.WishListRequest(id=item_id, buyer_address=buyer_address)
    response = stub.AddToWishList(request)
    print("Buyer prints:")
    if response.result == response.SUCCESS:
        print("SUCCESS")
    else:
        print("FAIL")


def rate_item(stub, item_id, buyer_address, rating):
    request = shopping_pb2.RateRequest(
        id=item_id, buyer_address=buyer_address, rating=rating
    )
    response = stub.RateItem(request)
    print("Buyer prints:")
    if response.result == response.SUCCESS:
        print("SUCCESS")
    else:
        print("FAIL")

def main(ip,port):
    logging.basicConfig()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    shopping_pb2_grpc.add_NotificationServicer_to_server(NotificationServicer(), server)
    server.add_insecure_port("[::]:50054")
    server.start()
    print("Buyer notification Server started")
    buyer_address = "localhost:50054"
    with grpc.insecure_channel("localhost:50052") as market_channel:
        market_stub = shopping_pb2_grpc.MarketStub(market_channel)
        # Replace with actual Market address
        # notify_channel = grpc.insecure_channel(
        #     "localhost:50052"
        # )  # Replace with actual Notification address
        # notify_stub = NotifyClientStub(notify_channel)

        # Create a gRPC server for NotifyClient service
        # notify_server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        # add_NotifyClientServicer_to_server(NotifyClientServicerImpl(), notify_server)
        # notify_server.add_insecure_port(buyer_address)
        # notify_server.start()

        # Example usage of functionalities
        unique_id = str(uuid.uuid1())
        # menu driven
        while True:
            print("1. Search Item")
            print("2. Buy Item")
            print("3. Add to Wishlist")
            print("4. Rate Item")
            print("5.exit")
            choice = int(input("Enter choice: "))
            if choice == 1:
                item_id = input("Enter item name: ")
                while True:
                    print(
                        "Enter 1 for Electronics\nEnter 2 for FASHION\nEnter 3 for Others\nEnter 4 for ANY"
                    )
                    category = int(input("Enter category: "))
                    if category >= 1 and category <= 4:
                        search_item(market_stub, item_id, category)
                        break
            elif choice == 2:
                item_id = int(input("Enter item id: "))
                quantity = int(input("Enter quantity: "))
                buy_item(market_stub, item_id, quantity, buyer_address)
            elif choice == 3:
                item_id = int(input("Enter item id: "))
                add_to_wishlist(market_stub, item_id, buyer_address)
            elif choice == 4:
                item_id = int(input("Enter item id to rate: "))
                rating = int(input("Enter rating: "))
                rate_item(market_stub, item_id, buyer_address, rating)
            else:
                break

    server.wait_for_termination()


if __name__ == "__main__":
    main()