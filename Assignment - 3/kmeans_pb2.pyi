from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class mapreturn(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class Reducereturn(_message.Message):
    __slots__ = ("success", "reduce_output")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    REDUCE_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    success: bool
    reduce_output: str
    def __init__(self, success: bool = ..., reduce_output: _Optional[str] = ...) -> None: ...

class centroids(_message.Message):
    __slots__ = ("x", "y")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ...) -> None: ...

class reducerinput(_message.Message):
    __slots__ = ("reducer_id", "centroidlist", "num_mappers", "mappers")
    REDUCER_ID_FIELD_NUMBER: _ClassVar[int]
    CENTROIDLIST_FIELD_NUMBER: _ClassVar[int]
    NUM_MAPPERS_FIELD_NUMBER: _ClassVar[int]
    MAPPERS_FIELD_NUMBER: _ClassVar[int]
    reducer_id: int
    centroidlist: _containers.RepeatedCompositeFieldContainer[centroids]
    num_mappers: int
    mappers: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, reducer_id: _Optional[int] = ..., centroidlist: _Optional[_Iterable[_Union[centroids, _Mapping]]] = ..., num_mappers: _Optional[int] = ..., mappers: _Optional[_Iterable[str]] = ...) -> None: ...

class InputSplitRequest(_message.Message):
    __slots__ = ("startidx", "endidx", "centroidlist", "mapper_id", "no_reducers")
    STARTIDX_FIELD_NUMBER: _ClassVar[int]
    ENDIDX_FIELD_NUMBER: _ClassVar[int]
    CENTROIDLIST_FIELD_NUMBER: _ClassVar[int]
    MAPPER_ID_FIELD_NUMBER: _ClassVar[int]
    NO_REDUCERS_FIELD_NUMBER: _ClassVar[int]
    startidx: int
    endidx: int
    centroidlist: _containers.RepeatedCompositeFieldContainer[centroids]
    mapper_id: int
    no_reducers: int
    def __init__(self, startidx: _Optional[int] = ..., endidx: _Optional[int] = ..., centroidlist: _Optional[_Iterable[_Union[centroids, _Mapping]]] = ..., mapper_id: _Optional[int] = ..., no_reducers: _Optional[int] = ...) -> None: ...

class trio(_message.Message):
    __slots__ = ("x", "y", "centroidId")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    CENTROIDID_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    centroidId: int
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ..., centroidId: _Optional[int] = ...) -> None: ...

class ReducerInputRequest(_message.Message):
    __slots__ = ("reducer_id",)
    REDUCER_ID_FIELD_NUMBER: _ClassVar[int]
    reducer_id: int
    def __init__(self, reducer_id: _Optional[int] = ...) -> None: ...

class ReducerOutput(_message.Message):
    __slots__ = ("success", "map_outputs")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MAP_OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    map_outputs: _containers.RepeatedCompositeFieldContainer[trio]
    def __init__(self, success: bool = ..., map_outputs: _Optional[_Iterable[_Union[trio, _Mapping]]] = ...) -> None: ...
