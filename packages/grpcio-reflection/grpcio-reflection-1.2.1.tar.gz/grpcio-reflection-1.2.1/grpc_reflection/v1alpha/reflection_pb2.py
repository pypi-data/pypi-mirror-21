# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: grpc_reflection/v1alpha/reflection.proto

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
  name='grpc_reflection/v1alpha/reflection.proto',
  package='grpc.reflection.v1alpha',
  syntax='proto3',
  serialized_pb=_b('\n(grpc_reflection/v1alpha/reflection.proto\x12\x17grpc.reflection.v1alpha\"\x8a\x02\n\x17ServerReflectionRequest\x12\x0c\n\x04host\x18\x01 \x01(\t\x12\x1a\n\x10\x66ile_by_filename\x18\x03 \x01(\tH\x00\x12 \n\x16\x66ile_containing_symbol\x18\x04 \x01(\tH\x00\x12N\n\x19\x66ile_containing_extension\x18\x05 \x01(\x0b\x32).grpc.reflection.v1alpha.ExtensionRequestH\x00\x12\'\n\x1d\x61ll_extension_numbers_of_type\x18\x06 \x01(\tH\x00\x12\x17\n\rlist_services\x18\x07 \x01(\tH\x00\x42\x11\n\x0fmessage_request\"E\n\x10\x45xtensionRequest\x12\x17\n\x0f\x63ontaining_type\x18\x01 \x01(\t\x12\x18\n\x10\x65xtension_number\x18\x02 \x01(\x05\"\xd1\x03\n\x18ServerReflectionResponse\x12\x12\n\nvalid_host\x18\x01 \x01(\t\x12J\n\x10original_request\x18\x02 \x01(\x0b\x32\x30.grpc.reflection.v1alpha.ServerReflectionRequest\x12S\n\x18\x66ile_descriptor_response\x18\x04 \x01(\x0b\x32/.grpc.reflection.v1alpha.FileDescriptorResponseH\x00\x12Z\n\x1e\x61ll_extension_numbers_response\x18\x05 \x01(\x0b\x32\x30.grpc.reflection.v1alpha.ExtensionNumberResponseH\x00\x12N\n\x16list_services_response\x18\x06 \x01(\x0b\x32,.grpc.reflection.v1alpha.ListServiceResponseH\x00\x12@\n\x0e\x65rror_response\x18\x07 \x01(\x0b\x32&.grpc.reflection.v1alpha.ErrorResponseH\x00\x42\x12\n\x10message_response\"7\n\x16\x46ileDescriptorResponse\x12\x1d\n\x15\x66ile_descriptor_proto\x18\x01 \x03(\x0c\"K\n\x17\x45xtensionNumberResponse\x12\x16\n\x0e\x62\x61se_type_name\x18\x01 \x01(\t\x12\x18\n\x10\x65xtension_number\x18\x02 \x03(\x05\"P\n\x13ListServiceResponse\x12\x39\n\x07service\x18\x01 \x03(\x0b\x32(.grpc.reflection.v1alpha.ServiceResponse\"\x1f\n\x0fServiceResponse\x12\x0c\n\x04name\x18\x01 \x01(\t\":\n\rErrorResponse\x12\x12\n\nerror_code\x18\x01 \x01(\x05\x12\x15\n\rerror_message\x18\x02 \x01(\t2\x93\x01\n\x10ServerReflection\x12\x7f\n\x14ServerReflectionInfo\x12\x30.grpc.reflection.v1alpha.ServerReflectionRequest\x1a\x31.grpc.reflection.v1alpha.ServerReflectionResponse(\x01\x30\x01\x62\x06proto3')
)
_sym_db.RegisterFileDescriptor(DESCRIPTOR)




_SERVERREFLECTIONREQUEST = _descriptor.Descriptor(
  name='ServerReflectionRequest',
  full_name='grpc.reflection.v1alpha.ServerReflectionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='host', full_name='grpc.reflection.v1alpha.ServerReflectionRequest.host', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='file_by_filename', full_name='grpc.reflection.v1alpha.ServerReflectionRequest.file_by_filename', index=1,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='file_containing_symbol', full_name='grpc.reflection.v1alpha.ServerReflectionRequest.file_containing_symbol', index=2,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='file_containing_extension', full_name='grpc.reflection.v1alpha.ServerReflectionRequest.file_containing_extension', index=3,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='all_extension_numbers_of_type', full_name='grpc.reflection.v1alpha.ServerReflectionRequest.all_extension_numbers_of_type', index=4,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='list_services', full_name='grpc.reflection.v1alpha.ServerReflectionRequest.list_services', index=5,
      number=7, type=9, cpp_type=9, label=1,
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
    _descriptor.OneofDescriptor(
      name='message_request', full_name='grpc.reflection.v1alpha.ServerReflectionRequest.message_request',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=70,
  serialized_end=336,
)


_EXTENSIONREQUEST = _descriptor.Descriptor(
  name='ExtensionRequest',
  full_name='grpc.reflection.v1alpha.ExtensionRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='containing_type', full_name='grpc.reflection.v1alpha.ExtensionRequest.containing_type', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='extension_number', full_name='grpc.reflection.v1alpha.ExtensionRequest.extension_number', index=1,
      number=2, type=5, cpp_type=1, label=1,
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
  serialized_start=338,
  serialized_end=407,
)


_SERVERREFLECTIONRESPONSE = _descriptor.Descriptor(
  name='ServerReflectionResponse',
  full_name='grpc.reflection.v1alpha.ServerReflectionResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='valid_host', full_name='grpc.reflection.v1alpha.ServerReflectionResponse.valid_host', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='original_request', full_name='grpc.reflection.v1alpha.ServerReflectionResponse.original_request', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='file_descriptor_response', full_name='grpc.reflection.v1alpha.ServerReflectionResponse.file_descriptor_response', index=2,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='all_extension_numbers_response', full_name='grpc.reflection.v1alpha.ServerReflectionResponse.all_extension_numbers_response', index=3,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='list_services_response', full_name='grpc.reflection.v1alpha.ServerReflectionResponse.list_services_response', index=4,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='error_response', full_name='grpc.reflection.v1alpha.ServerReflectionResponse.error_response', index=5,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
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
    _descriptor.OneofDescriptor(
      name='message_response', full_name='grpc.reflection.v1alpha.ServerReflectionResponse.message_response',
      index=0, containing_type=None, fields=[]),
  ],
  serialized_start=410,
  serialized_end=875,
)


_FILEDESCRIPTORRESPONSE = _descriptor.Descriptor(
  name='FileDescriptorResponse',
  full_name='grpc.reflection.v1alpha.FileDescriptorResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='file_descriptor_proto', full_name='grpc.reflection.v1alpha.FileDescriptorResponse.file_descriptor_proto', index=0,
      number=1, type=12, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=877,
  serialized_end=932,
)


_EXTENSIONNUMBERRESPONSE = _descriptor.Descriptor(
  name='ExtensionNumberResponse',
  full_name='grpc.reflection.v1alpha.ExtensionNumberResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='base_type_name', full_name='grpc.reflection.v1alpha.ExtensionNumberResponse.base_type_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='extension_number', full_name='grpc.reflection.v1alpha.ExtensionNumberResponse.extension_number', index=1,
      number=2, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=934,
  serialized_end=1009,
)


_LISTSERVICERESPONSE = _descriptor.Descriptor(
  name='ListServiceResponse',
  full_name='grpc.reflection.v1alpha.ListServiceResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='service', full_name='grpc.reflection.v1alpha.ListServiceResponse.service', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=1011,
  serialized_end=1091,
)


_SERVICERESPONSE = _descriptor.Descriptor(
  name='ServiceResponse',
  full_name='grpc.reflection.v1alpha.ServiceResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='name', full_name='grpc.reflection.v1alpha.ServiceResponse.name', index=0,
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
  serialized_start=1093,
  serialized_end=1124,
)


_ERRORRESPONSE = _descriptor.Descriptor(
  name='ErrorResponse',
  full_name='grpc.reflection.v1alpha.ErrorResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='error_code', full_name='grpc.reflection.v1alpha.ErrorResponse.error_code', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='error_message', full_name='grpc.reflection.v1alpha.ErrorResponse.error_message', index=1,
      number=2, type=9, cpp_type=9, label=1,
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
  serialized_start=1126,
  serialized_end=1184,
)

_SERVERREFLECTIONREQUEST.fields_by_name['file_containing_extension'].message_type = _EXTENSIONREQUEST
_SERVERREFLECTIONREQUEST.oneofs_by_name['message_request'].fields.append(
  _SERVERREFLECTIONREQUEST.fields_by_name['file_by_filename'])
_SERVERREFLECTIONREQUEST.fields_by_name['file_by_filename'].containing_oneof = _SERVERREFLECTIONREQUEST.oneofs_by_name['message_request']
_SERVERREFLECTIONREQUEST.oneofs_by_name['message_request'].fields.append(
  _SERVERREFLECTIONREQUEST.fields_by_name['file_containing_symbol'])
_SERVERREFLECTIONREQUEST.fields_by_name['file_containing_symbol'].containing_oneof = _SERVERREFLECTIONREQUEST.oneofs_by_name['message_request']
_SERVERREFLECTIONREQUEST.oneofs_by_name['message_request'].fields.append(
  _SERVERREFLECTIONREQUEST.fields_by_name['file_containing_extension'])
_SERVERREFLECTIONREQUEST.fields_by_name['file_containing_extension'].containing_oneof = _SERVERREFLECTIONREQUEST.oneofs_by_name['message_request']
_SERVERREFLECTIONREQUEST.oneofs_by_name['message_request'].fields.append(
  _SERVERREFLECTIONREQUEST.fields_by_name['all_extension_numbers_of_type'])
_SERVERREFLECTIONREQUEST.fields_by_name['all_extension_numbers_of_type'].containing_oneof = _SERVERREFLECTIONREQUEST.oneofs_by_name['message_request']
_SERVERREFLECTIONREQUEST.oneofs_by_name['message_request'].fields.append(
  _SERVERREFLECTIONREQUEST.fields_by_name['list_services'])
_SERVERREFLECTIONREQUEST.fields_by_name['list_services'].containing_oneof = _SERVERREFLECTIONREQUEST.oneofs_by_name['message_request']
_SERVERREFLECTIONRESPONSE.fields_by_name['original_request'].message_type = _SERVERREFLECTIONREQUEST
_SERVERREFLECTIONRESPONSE.fields_by_name['file_descriptor_response'].message_type = _FILEDESCRIPTORRESPONSE
_SERVERREFLECTIONRESPONSE.fields_by_name['all_extension_numbers_response'].message_type = _EXTENSIONNUMBERRESPONSE
_SERVERREFLECTIONRESPONSE.fields_by_name['list_services_response'].message_type = _LISTSERVICERESPONSE
_SERVERREFLECTIONRESPONSE.fields_by_name['error_response'].message_type = _ERRORRESPONSE
_SERVERREFLECTIONRESPONSE.oneofs_by_name['message_response'].fields.append(
  _SERVERREFLECTIONRESPONSE.fields_by_name['file_descriptor_response'])
_SERVERREFLECTIONRESPONSE.fields_by_name['file_descriptor_response'].containing_oneof = _SERVERREFLECTIONRESPONSE.oneofs_by_name['message_response']
_SERVERREFLECTIONRESPONSE.oneofs_by_name['message_response'].fields.append(
  _SERVERREFLECTIONRESPONSE.fields_by_name['all_extension_numbers_response'])
_SERVERREFLECTIONRESPONSE.fields_by_name['all_extension_numbers_response'].containing_oneof = _SERVERREFLECTIONRESPONSE.oneofs_by_name['message_response']
_SERVERREFLECTIONRESPONSE.oneofs_by_name['message_response'].fields.append(
  _SERVERREFLECTIONRESPONSE.fields_by_name['list_services_response'])
_SERVERREFLECTIONRESPONSE.fields_by_name['list_services_response'].containing_oneof = _SERVERREFLECTIONRESPONSE.oneofs_by_name['message_response']
_SERVERREFLECTIONRESPONSE.oneofs_by_name['message_response'].fields.append(
  _SERVERREFLECTIONRESPONSE.fields_by_name['error_response'])
_SERVERREFLECTIONRESPONSE.fields_by_name['error_response'].containing_oneof = _SERVERREFLECTIONRESPONSE.oneofs_by_name['message_response']
_LISTSERVICERESPONSE.fields_by_name['service'].message_type = _SERVICERESPONSE
DESCRIPTOR.message_types_by_name['ServerReflectionRequest'] = _SERVERREFLECTIONREQUEST
DESCRIPTOR.message_types_by_name['ExtensionRequest'] = _EXTENSIONREQUEST
DESCRIPTOR.message_types_by_name['ServerReflectionResponse'] = _SERVERREFLECTIONRESPONSE
DESCRIPTOR.message_types_by_name['FileDescriptorResponse'] = _FILEDESCRIPTORRESPONSE
DESCRIPTOR.message_types_by_name['ExtensionNumberResponse'] = _EXTENSIONNUMBERRESPONSE
DESCRIPTOR.message_types_by_name['ListServiceResponse'] = _LISTSERVICERESPONSE
DESCRIPTOR.message_types_by_name['ServiceResponse'] = _SERVICERESPONSE
DESCRIPTOR.message_types_by_name['ErrorResponse'] = _ERRORRESPONSE

ServerReflectionRequest = _reflection.GeneratedProtocolMessageType('ServerReflectionRequest', (_message.Message,), dict(
  DESCRIPTOR = _SERVERREFLECTIONREQUEST,
  __module__ = 'grpc_reflection.v1alpha.reflection_pb2'
  # @@protoc_insertion_point(class_scope:grpc.reflection.v1alpha.ServerReflectionRequest)
  ))
_sym_db.RegisterMessage(ServerReflectionRequest)

ExtensionRequest = _reflection.GeneratedProtocolMessageType('ExtensionRequest', (_message.Message,), dict(
  DESCRIPTOR = _EXTENSIONREQUEST,
  __module__ = 'grpc_reflection.v1alpha.reflection_pb2'
  # @@protoc_insertion_point(class_scope:grpc.reflection.v1alpha.ExtensionRequest)
  ))
_sym_db.RegisterMessage(ExtensionRequest)

ServerReflectionResponse = _reflection.GeneratedProtocolMessageType('ServerReflectionResponse', (_message.Message,), dict(
  DESCRIPTOR = _SERVERREFLECTIONRESPONSE,
  __module__ = 'grpc_reflection.v1alpha.reflection_pb2'
  # @@protoc_insertion_point(class_scope:grpc.reflection.v1alpha.ServerReflectionResponse)
  ))
_sym_db.RegisterMessage(ServerReflectionResponse)

FileDescriptorResponse = _reflection.GeneratedProtocolMessageType('FileDescriptorResponse', (_message.Message,), dict(
  DESCRIPTOR = _FILEDESCRIPTORRESPONSE,
  __module__ = 'grpc_reflection.v1alpha.reflection_pb2'
  # @@protoc_insertion_point(class_scope:grpc.reflection.v1alpha.FileDescriptorResponse)
  ))
_sym_db.RegisterMessage(FileDescriptorResponse)

ExtensionNumberResponse = _reflection.GeneratedProtocolMessageType('ExtensionNumberResponse', (_message.Message,), dict(
  DESCRIPTOR = _EXTENSIONNUMBERRESPONSE,
  __module__ = 'grpc_reflection.v1alpha.reflection_pb2'
  # @@protoc_insertion_point(class_scope:grpc.reflection.v1alpha.ExtensionNumberResponse)
  ))
_sym_db.RegisterMessage(ExtensionNumberResponse)

ListServiceResponse = _reflection.GeneratedProtocolMessageType('ListServiceResponse', (_message.Message,), dict(
  DESCRIPTOR = _LISTSERVICERESPONSE,
  __module__ = 'grpc_reflection.v1alpha.reflection_pb2'
  # @@protoc_insertion_point(class_scope:grpc.reflection.v1alpha.ListServiceResponse)
  ))
_sym_db.RegisterMessage(ListServiceResponse)

ServiceResponse = _reflection.GeneratedProtocolMessageType('ServiceResponse', (_message.Message,), dict(
  DESCRIPTOR = _SERVICERESPONSE,
  __module__ = 'grpc_reflection.v1alpha.reflection_pb2'
  # @@protoc_insertion_point(class_scope:grpc.reflection.v1alpha.ServiceResponse)
  ))
_sym_db.RegisterMessage(ServiceResponse)

ErrorResponse = _reflection.GeneratedProtocolMessageType('ErrorResponse', (_message.Message,), dict(
  DESCRIPTOR = _ERRORRESPONSE,
  __module__ = 'grpc_reflection.v1alpha.reflection_pb2'
  # @@protoc_insertion_point(class_scope:grpc.reflection.v1alpha.ErrorResponse)
  ))
_sym_db.RegisterMessage(ErrorResponse)


try:
  # THESE ELEMENTS WILL BE DEPRECATED.
  # Please use the generated *_pb2_grpc.py files instead.
  import grpc
  from grpc.framework.common import cardinality
  from grpc.framework.interfaces.face import utilities as face_utilities
  from grpc.beta import implementations as beta_implementations
  from grpc.beta import interfaces as beta_interfaces


  class ServerReflectionStub(object):

    def __init__(self, channel):
      """Constructor.

      Args:
        channel: A grpc.Channel.
      """
      self.ServerReflectionInfo = channel.stream_stream(
          '/grpc.reflection.v1alpha.ServerReflection/ServerReflectionInfo',
          request_serializer=ServerReflectionRequest.SerializeToString,
          response_deserializer=ServerReflectionResponse.FromString,
          )


  class ServerReflectionServicer(object):

    def ServerReflectionInfo(self, request_iterator, context):
      """The reflection service is structured as a bidirectional stream, ensuring
      all related requests go to a single server.
      """
      context.set_code(grpc.StatusCode.UNIMPLEMENTED)
      context.set_details('Method not implemented!')
      raise NotImplementedError('Method not implemented!')


  def add_ServerReflectionServicer_to_server(servicer, server):
    rpc_method_handlers = {
        'ServerReflectionInfo': grpc.stream_stream_rpc_method_handler(
            servicer.ServerReflectionInfo,
            request_deserializer=ServerReflectionRequest.FromString,
            response_serializer=ServerReflectionResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        'grpc.reflection.v1alpha.ServerReflection', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


  class BetaServerReflectionServicer(object):
    """The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This class was generated
    only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0."""
    def ServerReflectionInfo(self, request_iterator, context):
      """The reflection service is structured as a bidirectional stream, ensuring
      all related requests go to a single server.
      """
      context.code(beta_interfaces.StatusCode.UNIMPLEMENTED)


  class BetaServerReflectionStub(object):
    """The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This class was generated
    only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0."""
    def ServerReflectionInfo(self, request_iterator, timeout, metadata=None, with_call=False, protocol_options=None):
      """The reflection service is structured as a bidirectional stream, ensuring
      all related requests go to a single server.
      """
      raise NotImplementedError()


  def beta_create_ServerReflection_server(servicer, pool=None, pool_size=None, default_timeout=None, maximum_timeout=None):
    """The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This function was
    generated only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0"""
    request_deserializers = {
      ('grpc.reflection.v1alpha.ServerReflection', 'ServerReflectionInfo'): ServerReflectionRequest.FromString,
    }
    response_serializers = {
      ('grpc.reflection.v1alpha.ServerReflection', 'ServerReflectionInfo'): ServerReflectionResponse.SerializeToString,
    }
    method_implementations = {
      ('grpc.reflection.v1alpha.ServerReflection', 'ServerReflectionInfo'): face_utilities.stream_stream_inline(servicer.ServerReflectionInfo),
    }
    server_options = beta_implementations.server_options(request_deserializers=request_deserializers, response_serializers=response_serializers, thread_pool=pool, thread_pool_size=pool_size, default_timeout=default_timeout, maximum_timeout=maximum_timeout)
    return beta_implementations.server(method_implementations, options=server_options)


  def beta_create_ServerReflection_stub(channel, host=None, metadata_transformer=None, pool=None, pool_size=None):
    """The Beta API is deprecated for 0.15.0 and later.

    It is recommended to use the GA API (classes and functions in this
    file not marked beta) for all further purposes. This function was
    generated only to ease transition from grpcio<0.15.0 to grpcio>=0.15.0"""
    request_serializers = {
      ('grpc.reflection.v1alpha.ServerReflection', 'ServerReflectionInfo'): ServerReflectionRequest.SerializeToString,
    }
    response_deserializers = {
      ('grpc.reflection.v1alpha.ServerReflection', 'ServerReflectionInfo'): ServerReflectionResponse.FromString,
    }
    cardinalities = {
      'ServerReflectionInfo': cardinality.Cardinality.STREAM_STREAM,
    }
    stub_options = beta_implementations.stub_options(host=host, metadata_transformer=metadata_transformer, request_serializers=request_serializers, response_deserializers=response_deserializers, thread_pool=pool, thread_pool_size=pool_size)
    return beta_implementations.dynamic_stub(channel, 'grpc.reflection.v1alpha.ServerReflection', cardinalities, options=stub_options)
except ImportError:
  pass
# @@protoc_insertion_point(module_scope)
