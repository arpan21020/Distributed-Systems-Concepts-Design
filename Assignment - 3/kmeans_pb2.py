# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: kmeans.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0ckmeans.proto\"\x1c\n\tmapreturn\x12\x0f\n\x07success\x18\x01 \x01(\x08\"6\n\x0cReducereturn\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x15\n\rreduce_output\x18\x02 \x01(\t\"!\n\tcentroids\x12\t\n\x01x\x18\x01 \x01(\x02\x12\t\n\x01y\x18\x02 \x01(\x02\"z\n\x0creducerinput\x12\x12\n\nreducer_id\x18\x01 \x01(\x05\x12 \n\x0c\x63\x65ntroidlist\x18\x02 \x03(\x0b\x32\n.centroids\x12\x13\n\x0bnum_mappers\x18\x03 \x01(\x05\x12\x0f\n\x07mappers\x18\x04 \x03(\t\x12\x0e\n\x06second\x18\x05 \x01(\x05\"\x8f\x01\n\x11InputSplitRequest\x12\x10\n\x08startidx\x18\x01 \x01(\x05\x12\x0e\n\x06\x65ndidx\x18\x02 \x01(\x05\x12 \n\x0c\x63\x65ntroidlist\x18\x03 \x03(\x0b\x32\n.centroids\x12\x11\n\tmapper_id\x18\x04 \x01(\x05\x12\x13\n\x0bno_reducers\x18\x05 \x01(\x05\x12\x0e\n\x06\x61ppend\x18\x06 \x01(\x08\"0\n\x04trio\x12\t\n\x01x\x18\x01 \x01(\x02\x12\t\n\x01y\x18\x02 \x01(\x02\x12\x12\n\ncentroidId\x18\x03 \x01(\x05\")\n\x13ReducerInputRequest\x12\x12\n\nreducer_id\x18\x01 \x01(\x05\"<\n\rReducerOutput\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x1a\n\x0bmap_outputs\x18\x02 \x03(\x0b\x32\x05.trio2q\n\x06Mapper\x12\x38\n\x10GivereducerInput\x12\x14.ReducerInputRequest\x1a\x0e.ReducerOutput\x12-\n\x0b\x63\x61ll_mapper\x12\x12.InputSplitRequest\x1a\n.mapreturn27\n\x07Reducer\x12,\n\x0c\x63\x61ll_reducer\x12\r.reducerinput\x1a\r.Reducereturnb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'kmeans_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_MAPRETURN']._serialized_start=16
  _globals['_MAPRETURN']._serialized_end=44
  _globals['_REDUCERETURN']._serialized_start=46
  _globals['_REDUCERETURN']._serialized_end=100
  _globals['_CENTROIDS']._serialized_start=102
  _globals['_CENTROIDS']._serialized_end=135
  _globals['_REDUCERINPUT']._serialized_start=137
  _globals['_REDUCERINPUT']._serialized_end=259
  _globals['_INPUTSPLITREQUEST']._serialized_start=262
  _globals['_INPUTSPLITREQUEST']._serialized_end=405
  _globals['_TRIO']._serialized_start=407
  _globals['_TRIO']._serialized_end=455
  _globals['_REDUCERINPUTREQUEST']._serialized_start=457
  _globals['_REDUCERINPUTREQUEST']._serialized_end=498
  _globals['_REDUCEROUTPUT']._serialized_start=500
  _globals['_REDUCEROUTPUT']._serialized_end=560
  _globals['_MAPPER']._serialized_start=562
  _globals['_MAPPER']._serialized_end=675
  _globals['_REDUCER']._serialized_start=677
  _globals['_REDUCER']._serialized_end=732
# @@protoc_insertion_point(module_scope)
