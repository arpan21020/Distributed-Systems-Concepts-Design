import grpc
from concurrent import futures
import uuid
import logging

reg = False
import shopping_pb2
import shopping_pb2_grpc

class NotificationServicer(shopping_pb2_grpc.NotificationServicer):
    def NotifyClient(self, request, context):
        print("Seller prints:")
        print(request.message)
        return shopping_pb2.NotifyClientResponse(
            result=shopping_pb2.NotifyClientResponse.SUCCESS
        )


def register_seller(stub, seller_address, uniq):
    request = shopping_pb2.SellerInfo(address=seller_address, uuid=uniq)
    response = stub.RegisterSeller(request)
    print("Seller prints:")
    if response.result == response.SUCCESS:
        print("SUCCESS")
        print("Seller successfully registered")
        global reg
        reg = True
    else:
        print("FAIL")


def sell_item(
    stub,
    product_name,
    category,
    quantity,
    description,
    seller_address,
    price_per_unit,
    seller_uuid,
):
    print(category.upper())
    if category.upper() == "ELECTRONICS":
        category = shopping_pb2.Item.category.ELECTRONICS
    elif category.upper() == "FASHION":
        category = shopping_pb2.Item.category.FASHION
    else:
        category = shopping_pb2.Item.category.OTHERS
    request = shopping_pb2.Item(
        name=product_name,
        cat=category,
        quantity=quantity,
        description=description,
        seller_address=seller_address,
        price=price_per_unit,
        uuid=seller_uuid,
    )
    response = stub.SellItem(request)
    print("Seller prints:")
    if response.result == shopping_pb2.SellItemResponse.Result.SUCCESS:
        print(f"SUCCESS, Item ID: {response.item_id}")
    else:
        print("FAIL")


def update_item(stub, item_id, new_price, new_quantity, seller_address, seller_uuid):
    request = shopping_pb2.ItemUpdate(
        id=item_id,
        seller_address=seller_address,
        price=new_price,
        quantity=new_quantity,
        uuid=seller_uuid,
    )
    response = stub.UpdateItem(request)
    print("Seller prints:")
    if response.result == response.SUCCESS:
        print("SUCCESS")
    else:
        print("FAIL")


def delete_item(stub, item_id, seller_address, seller_uuid):
    request = shopping_pb2.ItemId(
        id=item_id, seller_address=seller_address, uuid=seller_uuid
    )
    response = stub.DeleteItem(request)
    print("Seller prints:")
    if response.result == response.SUCCESS:
        print("SUCCESS")
    else:
        print("FAIL")


def display_seller_items(stub, seller_address, seller_uuid):
    request = shopping_pb2.SellerInfo(
        address=seller_address, uuid=seller_uuid
    )
    response = stub.DisplaySellerItems(request)
    print("Seller prints:")
    for item in response.items:
        print(
            f"\nItem ID: {item.id}, Price: ${item.price}, Name: {item.name}, "
            f"Category: {item.category}\nDescription: {item.description}\n"
            f"Quantity Remaining: {item.quantity}\nRating: {item.rating} "
        )

def main():
    logging.basicConfig()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    shopping_pb2_grpc.add_NotificationServicer_to_server(NotificationServicer(), server)
    server.add_insecure_port("[::]:50050")
    server.start()
    print("Seller notification Server started")
    seller_address = "localhost:50050"

    with grpc.insecure_channel("localhost:50052") as market_channel:
        market_stub = shopping_pb2_grpc.MarketStub(market_channel)
        unique_id = str(uuid.uuid1())
        register_seller(
            market_stub,
            seller_address,
            unique_id,
        )
        print(reg)
        if reg:
            while True:
                print("1. Sell Item")
                print("2. Update Item")
                print("3. Delete Item")
                print("4. Display Seller Items")
                print("5. Exit")
                choice = int(input("Enter choice: "))
                if choice == 1:
                    product_name = input("Enter product name: ")
                    category = input("Enter category: ")
                    quantity = int(input("Enter quantity: "))
                    description = input("Enter description: ")
                    price_per_unit = float(input("Enter price per unit: "))
                    sell_item(
                        market_stub,
                        product_name,
                        category,
                        quantity,
                        description,
                        seller_address,
                        price_per_unit,
                        unique_id,
                    )
                elif choice == 2:
                    item_id = int(input("Enter item ID: "))
                    new_price = float(input("Enter new price: "))
                    new_quantity = int(input("Enter new quantity: "))
                    update_item(
                        market_stub,
                        item_id,
                        new_price,
                        new_quantity,
                        seller_address,
                        unique_id,
                    )
                elif choice == 3:
                    item_id = int(input("Enter item ID: "))
                    delete_item(
                        market_stub,
                        item_id,
                        seller_address,
                        unique_id,
                    )
                elif choice == 4:
                    display_seller_items(
                        market_stub,
                        seller_address,
                        unique_id,
                    )
                else:
                    break
    server.wait_for_termination()

if __name__ == "__main__":
    main()
