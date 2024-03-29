# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: counter.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='counter.proto',
  package='counter',
  syntax='proto3',
  serialized_pb=_b('\n\rcounter.proto\x12\x07\x63ounter\" \n\x10IncrementRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\"\"\n\x11IncrementResponse\x12\r\n\x05\x63ount\x18\x01 \x01(\x05\x32O\n\x07\x43ounter\x12\x44\n\tIncrement\x12\x19.counter.IncrementRequest\x1a\x1a.counter.IncrementResponse\"\x00\x62\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_INCREMENTREQUEST = _descriptor.Descriptor(
  name='IncrementRequest',
  full_name='counter.IncrementRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='counter.IncrementRequest.name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=26,
  serialized_end=58,
)


_INCREMENTRESPONSE = _descriptor.Descriptor(
  name='IncrementResponse',
  full_name='counter.IncrementResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='count', full_name='counter.IncrementResponse.count', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=60,
  serialized_end=94,
)

DESCRIPTOR.message_types_by_name['IncrementRequest'] = _INCREMENTREQUEST
DESCRIPTOR.message_types_by_name['IncrementResponse'] = _INCREMENTRESPONSE

IncrementRequest = _reflection.GeneratedProtocolMessageType('IncrementRequest', (_message.Message,), dict(
  DESCRIPTOR = _INCREMENTREQUEST,
  __module__ = 'counter_pb2'
  # @@protoc_insertion_point(class_scope:counter.IncrementRequest)
  ))
_sym_db.RegisterMessage(IncrementRequest)

IncrementResponse = _reflection.GeneratedProtocolMessageType('IncrementResponse', (_message.Message,), dict(
  DESCRIPTOR = _INCREMENTRESPONSE,
  __module__ = 'counter_pb2'
  # @@protoc_insertion_point(class_scope:counter.IncrementResponse)
  ))
_sym_db.RegisterMessage(IncrementResponse)


try:
  # THESE ELEMENTS WILL BE DEPRECATED.
  # Please use the generated *_pb2_grpc.py files instead.
  import grpc
  from grpc.framework.common import cardinality
  from grpc.framework.interfaces.face import utilities as face_utilities
  from grpc.beta import implementations as beta_implementations
  from grpc.beta import interfaces as beta_interfaces


  class CounterStub(object):

    def __init__(self, channel):
      """Constructor.

      Args:
        channel: A grpc.Channel.
      """
      self.Increment = channel.unary_unary(
          '/counter.Counter/Increment',
          request_serializer=IncrementRequest.SerializeToString,
          response_deserializer=IncrementResponse.FromString,
          )


  class CounterServicer(object):

    def Increment(self, request, context):
      context.set_code(grpc.StatusCode.UNIMPLEMENTED)
      context.set_details('Method not implemented!')
      raise NotImplementedError('Method not implemented!')


  def add_CounterServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'Increment': grpc.unary_unary_rpc_method_handler(
            servicer.Increment,
            request_deserializer=IncrementRequest.FromString,
            response_serializer=IncrementResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'counter.Counter', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


  class BetaCounterServicer(object):
    """The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This class was generated
    only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0."""
    def Increment(self, request, context):
      context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)


  class BetaCounterStub(object):
    """The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This class was generated
    only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0."""
    def Increment(self, request, timeout, metadata=None, with_call=False, protocol_options=None):
      raise NotImplementedError()
    Increment.future = None


  def beta_create_Counter_server(servicer, pool=None, pool_size=None, default_timeout=None, maximum_timeout=None):
    """The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This function was
    generated only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0"""
    request_deserializers = {
      ('counter.Counter', 'Increment'): IncrementRequest.FromString,
    }
    response_serializers = {
      ('counter.Counter', 'Increment'): IncrementResponse.SerializeToString,
    }
    method_implementations = {
      ('counter.Counter', 'Increment'): face_utilities.unary_unary_inline(servicer.Increment),
    }
    server_options = beta_implementations.server_options(request_deserializers=request_deserializers, response_serializers=response_serializers, thread_pool=pool, thread_pool_size=pool_size, default_timeout=default_timeout, maximum_timeout=maximum_timeout)
    return beta_implementations.server(method_implementations, options=server_options)


  def beta_create_Counter_stub(channel, host=None, metadata_transformer=None, pool=None, pool_size=None):
    """The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This function was
    generated only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0"""
    request_serializers = {
      ('counter.Counter', 'Increment'): IncrementRequest.SerializeToString,
    }
    response_deserializers = {
      ('counter.Counter', 'Increment'): IncrementResponse.FromString,
    }
    cardinalities = {
      'Increment': cardinality.Cardinality.UNARY_UNARY,
    }
    stub_options = beta_implementations.stub_options(host=host, metadata_transformer=metadata_transformer, request_serializers=request_serializers, response_deserializers=response_deserializers, thread_pool=pool, thread_pool_size=pool_size)
    return beta_implementations.dynamic_stub(channel, 'counter.Counter', cardinalities, options=stub_options)
except ImportError:
  pass
# @@protoc_insertion_point(module_scope)
