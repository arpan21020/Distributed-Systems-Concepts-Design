import grpc
from concurrent import futures
import shopping_pb2
import shopping_pb2_grpc
import logging

class MarketServicer(shopping_pb2_grpc.MarketServicer):
    def __init__(self):
        self.sellers = {} 
        self.items = {}  
        self.wishlists = {}  
        self.buyers = {} 
        self.rating={}
        self.rate={}

    def RegisterSeller(self, request, context):
        seller_address = request.address
        seller_uuid = request.uuid
        if seller_address in self.sellers:
            return shopping_pb2.RegisterSellerResponse(
                result=shopping_pb2.RegisterSellerResponse.FAIL
            )
        else:
            self.sellers[seller_address] = seller_uuid
            print(
                f"Market prints: Seller join request from {seller_address}, uuid = {seller_uuid}"
            )
            return shopping_pb2.RegisterSellerResponse(
                result=shopping_pb2.RegisterSellerResponse.SUCCESS
            )

    def SellItem(self, request, context):
        if request.uuid not in self.sellers.values():
            print("seller not registered yet")
            return shopping_pb2.SellItemResponse(
                result=shopping_pb2.SellItemResponse.FAIL
            )
        item_id = len(self.items) + 1
        item = {
            "id": item_id,
            "name": request.name,
            "category": request.cat,
            "quantity": request.quantity,
            "description": request.description,
            "seller_address": request.seller_address,
            "price_per_unit": request.price,
            "seller_uuid": request.uuid,
            "rating": 0.0,  # Initialize rating
        }
        self.items[item_id] = item
        print(f"Market prints: Sell Item request from {request.seller_address}")
        return shopping_pb2.SellItemResponse(
            result=shopping_pb2.SellItemResponse.Result.SUCCESS, item_id=item_id
        )

    def UpdateItem(self, request, context):
        item_id = request.id
        new_price = request.price
        new_quantity = request.quantity

        if item_id not in self.items:
            return shopping_pb2.UpdateItemResponse(
                result=shopping_pb2.UpdateItemResponse.FAIL
            )
        if self.items[item_id]["seller_uuid"] != request.uuid:
            return shopping_pb2.UpdateItemResponse(
                result=shopping_pb2.UpdateItemResponse.FAIL
            )

        item = self.items[item_id]
        item["price_per_unit"] = new_price
        item["quantity"] = new_quantity

        print(
            f"Market prints: Update Item {item_id} request from {request.seller_address} uuid = {request.uuid}"
        )

        for buyer_address, buyer_info in self.buyers.items():
            wishlist = buyer_info["wishlist"]
            if item["id"] in wishlist:
                with grpc.insecure_channel(buyer_address) as notify_channel:
                    notify_stub = shopping_pb2_grpc.NotificationStub(notify_channel)
                    mssg = (
                        "Your wishlist item has been updated\n item name : "
                        + item["name"]
                        + "\n item id : "
                        + str(item["id"])
                        + "\nNew item price : "
                        + str(item["price_per_unit"])
                        + "New item quantity : "
                        + str(item["quantity"])
                    )
                    response = notify_stub.NotifyClient(
                        shopping_pb2.Notification_mssg(message=mssg)
                    )
                    if response.result == response.SUCCESS:
                        print("SUCCESS")

        # print(self.items)
        return shopping_pb2.UpdateItemResponse(
            result=shopping_pb2.UpdateItemResponse.SUCCESS
        )

    def DeleteItem(self, request, context):
        # Implement logic to delete an item
        item_id = request.id
        if self.items[item_id]["seller_uuid"] != request.uuid:
            return shopping_pb2.DeleteItemResponse(
                result=shopping_pb2.DeleteItemResponse.FAIL
            )
        if item_id in self.items:
            del self.items[item_id]
            print(
                f"Market prints: Delete Item {item_id} request from {request.seller_address} uuid = {request.uuid}"
            )
            return shopping_pb2.DeleteItemResponse(
                result=shopping_pb2.DeleteItemResponse.SUCCESS
            )
        else:
            return shopping_pb2.DeleteItemResponse(
                result=shopping_pb2.DeleteItemResponse.FAIL
            )

    def DisplaySellerItems(self, request, context):
        # Implement logic to display items of a seller
        seller_address = request.address
        seller_uuid = request.uuid
        lst = []

        if (
            seller_address not in self.sellers
            or self.sellers[seller_address] != seller_uuid
        ):
            return shopping_pb2.DisplaySellerItemsResponse(items=lst)

        seller_items = [
            item for item in self.items.values() if item["seller_uuid"] == seller_uuid
        ]
        for i in seller_items:
            caty = i["category"]
            if caty == 0:
                caty = "ELECTRONICS"
            elif caty == 1:
                caty = "FASHION"
            else:
                caty = "OTHERS"

            lst.append(
                shopping_pb2.DisplayItem(
                    id=i["id"],
                    price=i["price_per_unit"],
                    name=i["name"],
                    category=caty,
                    description=i["description"],
                    quantity=i["quantity"],
                    rating=i["rating"],
                )
            )

        print(f"Market prints: Display Items request from {seller_address}")
        return shopping_pb2.DisplaySellerItemsResponse(items=lst)

    def SearchItem(self, request, context):
        item_name = request.name
        category = request.category
        print(
            f"Market prints: Search request for Item : {item_name}, Category: {category}"
        )
        lst = []
        if item_name == "":
            if category == 4:
                seller_items = [item for item in self.items.values()]
                for i in seller_items:
                    caty = i["category"]
                    if caty == 0:
                        caty = "ELECTRONICS"
                    elif caty == 1:
                        caty = "FASHION"
                    else:
                        caty = "OTHERS"
                    lst.append(
                        shopping_pb2.DisplayItem(
                            id=i["id"],
                            price=i["price_per_unit"],
                            name=i["name"],
                            category=caty,
                            description=i["description"],
                            quantity=i["quantity"],
                            rating=i["rating"],
                        )
                    )
                # print(f"Market prints: Search request for all items, Category: all")
                return shopping_pb2.SearchResponse(items=lst)
            else:
                seller_items = [
                    item
                    for item in self.items.values()
                    if item["category"] == category - 1
                ]
                if category == 0:
                    category = "ELECTRONICS"
                elif category == 1:
                    category = "FASHION"
                else:
                    category = "OTHERS"
                for i in seller_items:
                    lst.append(
                        shopping_pb2.DisplayItem(
                            id=i["id"],
                            price=i["price_per_unit"],
                            name=i["name"],
                            category=category,
                            description=i["description"],
                            quantity=i["quantity"],
                            rating=i["rating"],
                        )
                    )
                # print(
                #     f"Market prints: Search request for all items, Category: {category}"
                #
                return shopping_pb2.SearchResponse(items=lst)
        else:
            seller_items = [
                item
                for item in self.items.values()
                if item["name"].lower() == item_name.lower()
            ]
            if category !=seller_items[0]["category"]+1 and category!=4:
                print("No such item in entered category")
                return shopping_pb2.SearchResponse(items=lst)

            if category == 0:
                category = "ELECTRONICS"
            elif category == 1:
                category = "FASHION"
            else:
                category = "OTHERS"
            for item in seller_items:
                lst.append(
                    shopping_pb2.DisplayItem(
                        id=item["id"],
                        price=item["price_per_unit"],
                        name=item["name"],
                        category=category,
                        description=item["description"],
                        quantity=item["quantity"],
                        rating=item["rating"],
                    )
                )
            # print(
            #     f"Market prints: Search request for Item : {item_name}, Category: {category}"
            # )
            return shopping_pb2.SearchResponse(items=lst)

    def BuyItem(self, request, context):
        item_id = request.id
        quantity = request.quantity
        buyer_address = request.buyer_address

        if item_id not in self.items:
            print("item not found")
            return shopping_pb2.BuyItemResponse(
                result=shopping_pb2.BuyItemResponse.FAIL
            )

        item = self.items[item_id]
        if item["quantity"] < quantity:
            print("not enough quantity available")
            return shopping_pb2.BuyItemResponse(
                result=shopping_pb2.BuyItemResponse.FAIL
            )

        item["quantity"] -= quantity
        print(
            f"Market prints: Buy request {quantity} of item {item_id}, from {buyer_address}"
        )

        with grpc.insecure_channel(item["seller_address"]) as notify_channel:
            notify_stub = shopping_pb2_grpc.NotificationStub(notify_channel)
            mssg = (
                "Your item has been sold\n item name : "
                + item["name"]
                + "\n item id : "
                + str(item["id"])
                + "\nQuantity sold : "
                + str(quantity)
            )
            response = notify_stub.NotifyClient(
                shopping_pb2.Notification_mssg(message=mssg)
            )
            if response.result == response.SUCCESS:
                print("SUCCESS")
        return shopping_pb2.BuyItemResponse(result=shopping_pb2.BuyItemResponse.SUCCESS)

    def AddToWishList(self, request, context):
        # Implement logic to add an item to a buyer's wishlist
        item_id = request.id
        buyer_address = request.buyer_address

        if buyer_address not in self.buyers:
            self.buyers[buyer_address] = {"wishlist": []}

        if item_id in self.items:
            self.buyers[buyer_address]["wishlist"].append(item_id)
            print(
                f"Market prints: Wishlist request of item {item_id}, from {buyer_address}"
            )
            return shopping_pb2.AddToWishListResponse(
                result=shopping_pb2.AddToWishListResponse.SUCCESS
            )
        else:
            print("item id not found")
            return shopping_pb2.AddToWishListResponse(
                result=shopping_pb2.AddToWishListResponse.FAIL
            )

    def RateItem(self, request, context):
        # Implement logic to rate an item
        item_id = request.id
        buyer_address = request.buyer_address
        rating = request.rating

        if item_id not in self.items:
            print("item id not found")
            return shopping_pb2.RateResponse(result=shopping_pb2.RateResponse.FAIL)
        elif buyer_address in self.rating:
            if item_id in self.rating[buyer_address]:
                print("You have already rated this item")
                return shopping_pb2.RateResponse(result=shopping_pb2.RateResponse.FAIL)
        
        if buyer_address not in self.rating:
            self.rating[buyer_address] = []
        self.rating[buyer_address].append(item_id)

        if item_id not in self.rate:
            self.rate[item_id] = 0
        item = self.items[item_id]
        fin_rate= (item["rating"] * self.rate[item_id]+rating)/(self.rate[item_id]+1)
        self.rate[item_id] = self.rate[item_id] + 1
     
        item["rating"] = fin_rate

        print(
            f"Market prints: {buyer_address} rated item {item_id} with {rating} stars."
        )
        return shopping_pb2.RateResponse(result=shopping_pb2.RateResponse.SUCCESS)

def main():
    logging.basicConfig()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    shopping_pb2_grpc.add_MarketServicer_to_server(MarketServicer(), server)
    server.add_insecure_port("[::]:50052")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    main()
