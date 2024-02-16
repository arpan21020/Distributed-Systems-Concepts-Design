In this part, I have implemented a RPC distributed system using gRPC API in python. 
I have implemented a shopping platform in which we have one central market server and multiple buyers and sellers. 

I have implemented market server in market.py file. 
Command to start market server :
python3 market.py

I have implemented seller in seller.py file. In the seller, I have made server for listening to notifications sent by the market when any buyer buys that seller’s item.
Command to start a seller:
python3 seller.py <sellers ip> <sellers port> <server(market) ip>

I have implemented buyer in buyer.py file. In the buyer, I have made server for listening to notifications sent by the market when any seller updates the products wishlisted by the buyer.
Command to start a start a buyer:
python3 buyer.py <buyers ip> <buyers port> <server(market) ip>




