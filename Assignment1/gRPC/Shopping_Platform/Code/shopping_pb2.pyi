from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SellerInfo(_message.Message):
    __slots__ = ("address", "uuid")
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    address: str
    uuid: str
    def __init__(self, address: _Optional[str] = ..., uuid: _Optional[str] = ...) -> None: ...

class Item(_message.Message):
    __slots__ = ("name", "cat", "quantity", "description", "seller_address", "price", "uuid")
    class category(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        ELECTRONICS: _ClassVar[Item.category]
        FASHION: _ClassVar[Item.category]
        OTHERS: _ClassVar[Item.category]
    ELECTRONICS: Item.category
    FASHION: Item.category
    OTHERS: Item.category
    NAME_FIELD_NUMBER: _ClassVar[int]
    CAT_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SELLER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    name: str
    cat: Item.category
    quantity: int
    description: str
    seller_address: str
    price: float
    uuid: str
    def __init__(self, name: _Optional[str] = ..., cat: _Optional[_Union[Item.category, str]] = ..., quantity: _Optional[int] = ..., description: _Optional[str] = ..., seller_address: _Optional[str] = ..., price: _Optional[float] = ..., uuid: _Optional[str] = ...) -> None: ...

class ItemUpdate(_message.Message):
    __slots__ = ("id", "seller_address", "price", "quantity", "uuid")
    ID_FIELD_NUMBER: _ClassVar[int]
    SELLER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    id: int
    seller_address: str
    price: float
    quantity: int
    uuid: str
    def __init__(self, id: _Optional[int] = ..., seller_address: _Optional[str] = ..., price: _Optional[float] = ..., quantity: _Optional[int] = ..., uuid: _Optional[str] = ...) -> None: ...

class ItemId(_message.Message):
    __slots__ = ("id", "seller_address", "uuid")
    ID_FIELD_NUMBER: _ClassVar[int]
    SELLER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    id: int
    seller_address: str
    uuid: str
    def __init__(self, id: _Optional[int] = ..., seller_address: _Optional[str] = ..., uuid: _Optional[str] = ...) -> None: ...

class DisplaySellerItemsResponse(_message.Message):
    __slots__ = ("items",)
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[DisplayItem]
    def __init__(self, items: _Optional[_Iterable[_Union[DisplayItem, _Mapping]]] = ...) -> None: ...

class DisplayItem(_message.Message):
    __slots__ = ("id", "price", "name", "category", "description", "quantity", "rating")
    ID_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    RATING_FIELD_NUMBER: _ClassVar[int]
    id: int
    price: float
    name: str
    category: str
    description: str
    quantity: int
    rating: float
    def __init__(self, id: _Optional[int] = ..., price: _Optional[float] = ..., name: _Optional[str] = ..., category: _Optional[str] = ..., description: _Optional[str] = ..., quantity: _Optional[int] = ..., rating: _Optional[float] = ...) -> None: ...

class SearchRequest(_message.Message):
    __slots__ = ("name", "category")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    name: str
    category: int
    def __init__(self, name: _Optional[str] = ..., category: _Optional[int] = ...) -> None: ...

class SearchResponse(_message.Message):
    __slots__ = ("items",)
    ITEMS_FIELD_NUMBER: _ClassVar[int]
    items: _containers.RepeatedCompositeFieldContainer[DisplayItem]
    def __init__(self, items: _Optional[_Iterable[_Union[DisplayItem, _Mapping]]] = ...) -> None: ...

class BuyRequest(_message.Message):
    __slots__ = ("id", "quantity", "buyer_address")
    ID_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    BUYER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    id: int
    quantity: int
    buyer_address: str
    def __init__(self, id: _Optional[int] = ..., quantity: _Optional[int] = ..., buyer_address: _Optional[str] = ...) -> None: ...

class BuyItemResponse(_message.Message):
    __slots__ = ("result",)
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[BuyItemResponse.Result]
        FAIL: _ClassVar[BuyItemResponse.Result]
    SUCCESS: BuyItemResponse.Result
    FAIL: BuyItemResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: BuyItemResponse.Result
    def __init__(self, result: _Optional[_Union[BuyItemResponse.Result, str]] = ...) -> None: ...

class AddToWishListResponse(_message.Message):
    __slots__ = ("result",)
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[AddToWishListResponse.Result]
        FAIL: _ClassVar[AddToWishListResponse.Result]
    SUCCESS: AddToWishListResponse.Result
    FAIL: AddToWishListResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: AddToWishListResponse.Result
    def __init__(self, result: _Optional[_Union[AddToWishListResponse.Result, str]] = ...) -> None: ...

class WishListRequest(_message.Message):
    __slots__ = ("id", "buyer_address")
    ID_FIELD_NUMBER: _ClassVar[int]
    BUYER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    id: int
    buyer_address: str
    def __init__(self, id: _Optional[int] = ..., buyer_address: _Optional[str] = ...) -> None: ...

class RateRequest(_message.Message):
    __slots__ = ("id", "buyer_address", "rating")
    ID_FIELD_NUMBER: _ClassVar[int]
    BUYER_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    RATING_FIELD_NUMBER: _ClassVar[int]
    id: int
    buyer_address: str
    rating: int
    def __init__(self, id: _Optional[int] = ..., buyer_address: _Optional[str] = ..., rating: _Optional[int] = ...) -> None: ...

class RateResponse(_message.Message):
    __slots__ = ("result",)
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[RateResponse.Result]
        FAIL: _ClassVar[RateResponse.Result]
    SUCCESS: RateResponse.Result
    FAIL: RateResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: RateResponse.Result
    def __init__(self, result: _Optional[_Union[RateResponse.Result, str]] = ...) -> None: ...

class RegisterSellerResponse(_message.Message):
    __slots__ = ("result",)
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[RegisterSellerResponse.Result]
        FAIL: _ClassVar[RegisterSellerResponse.Result]
    SUCCESS: RegisterSellerResponse.Result
    FAIL: RegisterSellerResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: RegisterSellerResponse.Result
    def __init__(self, result: _Optional[_Union[RegisterSellerResponse.Result, str]] = ...) -> None: ...

class SellItemResponse(_message.Message):
    __slots__ = ("result", "item_id")
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[SellItemResponse.Result]
        FAIL: _ClassVar[SellItemResponse.Result]
    SUCCESS: SellItemResponse.Result
    FAIL: SellItemResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    ITEM_ID_FIELD_NUMBER: _ClassVar[int]
    result: SellItemResponse.Result
    item_id: int
    def __init__(self, result: _Optional[_Union[SellItemResponse.Result, str]] = ..., item_id: _Optional[int] = ...) -> None: ...

class UpdateItemResponse(_message.Message):
    __slots__ = ("result",)
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[UpdateItemResponse.Result]
        FAIL: _ClassVar[UpdateItemResponse.Result]
    SUCCESS: UpdateItemResponse.Result
    FAIL: UpdateItemResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: UpdateItemResponse.Result
    def __init__(self, result: _Optional[_Union[UpdateItemResponse.Result, str]] = ...) -> None: ...

class DeleteItemResponse(_message.Message):
    __slots__ = ("result",)
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[DeleteItemResponse.Result]
        FAIL: _ClassVar[DeleteItemResponse.Result]
    SUCCESS: DeleteItemResponse.Result
    FAIL: DeleteItemResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: DeleteItemResponse.Result
    def __init__(self, result: _Optional[_Union[DeleteItemResponse.Result, str]] = ...) -> None: ...

class NotifyClientResponse(_message.Message):
    __slots__ = ("result",)
    class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        SUCCESS: _ClassVar[NotifyClientResponse.Result]
        FAIL: _ClassVar[NotifyClientResponse.Result]
    SUCCESS: NotifyClientResponse.Result
    FAIL: NotifyClientResponse.Result
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: NotifyClientResponse.Result
    def __init__(self, result: _Optional[_Union[NotifyClientResponse.Result, str]] = ...) -> None: ...

class Notification_mssg(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...
