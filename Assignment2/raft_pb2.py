# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: raft.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nraft.proto\"&\n\x08KeyValue\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t\"4\n\x08LogEntry\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x0b\n\x03key\x18\x02 \x01(\t\x12\r\n\x05value\x18\x03 \x01(\t\"\xa8\x01\n\x12\x41ppendEntryRequest\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x10\n\x08leaderId\x18\x02 \x01(\t\x12\x14\n\x0cprevLogIndex\x18\x03 \x01(\x05\x12\x13\n\x0bprevLogTerm\x18\x04 \x01(\x05\x12\x1a\n\x07\x65ntries\x18\x05 \x03(\x0b\x32\t.LogEntry\x12\x14\n\x0cleaderCommit\x18\x06 \x01(\x05\x12\x15\n\rleaseInterval\x18\x07 \x01(\x02\"1\n\x10\x41ppendEntryReply\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x0f\n\x07success\x18\x02 \x01(\x08\"b\n\x12RequestVoteRequest\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x13\n\x0b\x63\x61ndidateId\x18\x02 \x01(\t\x12\x14\n\x0clastLogIndex\x18\x03 \x01(\x05\x12\x13\n\x0blastLogTerm\x18\x04 \x01(\x05\"I\n\x10RequestVoteReply\x12\x0c\n\x04term\x18\x01 \x01(\x05\x12\x0f\n\x07success\x18\x02 \x01(\x08\x12\x16\n\x0eoldLeaderLease\x18\x03 \x01(\x02\"\"\n\x0fServeClientArgs\x12\x0f\n\x07Request\x18\x01 \x01(\t\"C\n\x10ServeClientReply\x12\x0c\n\x04\x44\x61ta\x18\x01 \x01(\t\x12\x10\n\x08LeaderID\x18\x02 \x01(\t\x12\x0f\n\x07Success\x18\x03 \x01(\x08\x32\xb5\x01\n\x0bRaftCluster\x12\x37\n\x0b\x41ppendEntry\x12\x13.AppendEntryRequest\x1a\x11.AppendEntryReply\"\x00\x12\x37\n\x0bRequestVote\x12\x13.RequestVoteRequest\x1a\x11.RequestVoteReply\"\x00\x12\x34\n\x0bServeClient\x12\x10.ServeClientArgs\x1a\x11.ServeClientReply\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'raft_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_KEYVALUE']._serialized_start=14
  _globals['_KEYVALUE']._serialized_end=52
  _globals['_LOGENTRY']._serialized_start=54
  _globals['_LOGENTRY']._serialized_end=106
  _globals['_APPENDENTRYREQUEST']._serialized_start=109
  _globals['_APPENDENTRYREQUEST']._serialized_end=277
  _globals['_APPENDENTRYREPLY']._serialized_start=279
  _globals['_APPENDENTRYREPLY']._serialized_end=328
  _globals['_REQUESTVOTEREQUEST']._serialized_start=330
  _globals['_REQUESTVOTEREQUEST']._serialized_end=428
  _globals['_REQUESTVOTEREPLY']._serialized_start=430
  _globals['_REQUESTVOTEREPLY']._serialized_end=503
  _globals['_SERVECLIENTARGS']._serialized_start=505
  _globals['_SERVECLIENTARGS']._serialized_end=539
  _globals['_SERVECLIENTREPLY']._serialized_start=541
  _globals['_SERVECLIENTREPLY']._serialized_end=608
  _globals['_RAFTCLUSTER']._serialized_start=611
  _globals['_RAFTCLUSTER']._serialized_end=792
# @@protoc_insertion_point(module_scope)
