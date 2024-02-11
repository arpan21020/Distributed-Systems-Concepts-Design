# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import shopping_pb2 as shopping__pb2


class MarketStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.RegisterSeller = channel.unary_unary(
                '/shopping.Market/RegisterSeller',
                request_serializer=shopping__pb2.SellerInfo.SerializeToString,
                response_deserializer=shopping__pb2.RegisterSellerResponse.FromString,
                )
        self.SellItem = channel.unary_unary(
                '/shopping.Market/SellItem',
                request_serializer=shopping__pb2.Item.SerializeToString,
                response_deserializer=shopping__pb2.SellItemResponse.FromString,
                )
        self.UpdateItem = channel.unary_unary(
                '/shopping.Market/UpdateItem',
                request_serializer=shopping__pb2.ItemUpdate.SerializeToString,
                response_deserializer=shopping__pb2.UpdateItemResponse.FromString,
                )
        self.DeleteItem = channel.unary_unary(
                '/shopping.Market/DeleteItem',
                request_serializer=shopping__pb2.ItemId.SerializeToString,
                response_deserializer=shopping__pb2.DeleteItemResponse.FromString,
                )
        self.DisplaySellerItems = channel.unary_unary(
                '/shopping.Market/DisplaySellerItems',
                request_serializer=shopping__pb2.SellerInfo.SerializeToString,
                response_deserializer=shopping__pb2.DisplaySellerItemsResponse.FromString,
                )
        self.SearchItem = channel.unary_unary(
                '/shopping.Market/SearchItem',
                request_serializer=shopping__pb2.SearchRequest.SerializeToString,
                response_deserializer=shopping__pb2.SearchResponse.FromString,
                )
        self.BuyItem = channel.unary_unary(
                '/shopping.Market/BuyItem',
                request_serializer=shopping__pb2.BuyRequest.SerializeToString,
                response_deserializer=shopping__pb2.BuyItemResponse.FromString,
                )
        self.AddToWishList = channel.unary_unary(
                '/shopping.Market/AddToWishList',
                request_serializer=shopping__pb2.WishListRequest.SerializeToString,
                response_deserializer=shopping__pb2.AddToWishListResponse.FromString,
                )
        self.RateItem = channel.unary_unary(
                '/shopping.Market/RateItem',
                request_serializer=shopping__pb2.RateRequest.SerializeToString,
                response_deserializer=shopping__pb2.RateResponse.FromString,
                )


class MarketServicer(object):
    """Missing associated documentation comment in .proto file."""

    def RegisterSeller(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SellItem(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateItem(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteItem(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DisplaySellerItems(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SearchItem(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BuyItem(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AddToWishList(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RateItem(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MarketServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'RegisterSeller': grpc.unary_unary_rpc_method_handler(
                    servicer.RegisterSeller,
                    request_deserializer=shopping__pb2.SellerInfo.FromString,
                    response_serializer=shopping__pb2.RegisterSellerResponse.SerializeToString,
            ),
            'SellItem': grpc.unary_unary_rpc_method_handler(
                    servicer.SellItem,
                    request_deserializer=shopping__pb2.Item.FromString,
                    response_serializer=shopping__pb2.SellItemResponse.SerializeToString,
            ),
            'UpdateItem': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateItem,
                    request_deserializer=shopping__pb2.ItemUpdate.FromString,
                    response_serializer=shopping__pb2.UpdateItemResponse.SerializeToString,
            ),
            'DeleteItem': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteItem,
                    request_deserializer=shopping__pb2.ItemId.FromString,
                    response_serializer=shopping__pb2.DeleteItemResponse.SerializeToString,
            ),
            'DisplaySellerItems': grpc.unary_unary_rpc_method_handler(
                    servicer.DisplaySellerItems,
                    request_deserializer=shopping__pb2.SellerInfo.FromString,
                    response_serializer=shopping__pb2.DisplaySellerItemsResponse.SerializeToString,
            ),
            'SearchItem': grpc.unary_unary_rpc_method_handler(
                    servicer.SearchItem,
                    request_deserializer=shopping__pb2.SearchRequest.FromString,
                    response_serializer=shopping__pb2.SearchResponse.SerializeToString,
            ),
            'BuyItem': grpc.unary_unary_rpc_method_handler(
                    servicer.BuyItem,
                    request_deserializer=shopping__pb2.BuyRequest.FromString,
                    response_serializer=shopping__pb2.BuyItemResponse.SerializeToString,
            ),
            'AddToWishList': grpc.unary_unary_rpc_method_handler(
                    servicer.AddToWishList,
                    request_deserializer=shopping__pb2.WishListRequest.FromString,
                    response_serializer=shopping__pb2.AddToWishListResponse.SerializeToString,
            ),
            'RateItem': grpc.unary_unary_rpc_method_handler(
                    servicer.RateItem,
                    request_deserializer=shopping__pb2.RateRequest.FromString,
                    response_serializer=shopping__pb2.RateResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'shopping.Market', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Market(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def RegisterSeller(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/shopping.Market/RegisterSeller',
            shopping__pb2.SellerInfo.SerializeToString,
            shopping__pb2.RegisterSellerResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SellItem(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/shopping.Market/SellItem',
            shopping__pb2.Item.SerializeToString,
            shopping__pb2.SellItemResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UpdateItem(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/shopping.Market/UpdateItem',
            shopping__pb2.ItemUpdate.SerializeToString,
            shopping__pb2.UpdateItemResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DeleteItem(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/shopping.Market/DeleteItem',
            shopping__pb2.ItemId.SerializeToString,
            shopping__pb2.DeleteItemResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def DisplaySellerItems(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/shopping.Market/DisplaySellerItems',
            shopping__pb2.SellerInfo.SerializeToString,
            shopping__pb2.DisplaySellerItemsResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SearchItem(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/shopping.Market/SearchItem',
            shopping__pb2.SearchRequest.SerializeToString,
            shopping__pb2.SearchResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def BuyItem(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/shopping.Market/BuyItem',
            shopping__pb2.BuyRequest.SerializeToString,
            shopping__pb2.BuyItemResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def AddToWishList(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/shopping.Market/AddToWishList',
            shopping__pb2.WishListRequest.SerializeToString,
            shopping__pb2.AddToWishListResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RateItem(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/shopping.Market/RateItem',
            shopping__pb2.RateRequest.SerializeToString,
            shopping__pb2.RateResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class NotificationStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.NotifyClient = channel.unary_unary(
                '/shopping.Notification/NotifyClient',
                request_serializer=shopping__pb2.Notification_mssg.SerializeToString,
                response_deserializer=shopping__pb2.NotifyClientResponse.FromString,
                )


class NotificationServicer(object):
    """Missing associated documentation comment in .proto file."""

    def NotifyClient(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_NotificationServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'NotifyClient': grpc.unary_unary_rpc_method_handler(
                    servicer.NotifyClient,
                    request_deserializer=shopping__pb2.Notification_mssg.FromString,
                    response_serializer=shopping__pb2.NotifyClientResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'shopping.Notification', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Notification(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def NotifyClient(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/shopping.Notification/NotifyClient',
            shopping__pb2.Notification_mssg.SerializeToString,
            shopping__pb2.NotifyClientResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
