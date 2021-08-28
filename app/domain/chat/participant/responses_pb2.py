# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: responses.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='responses.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x0fresponses.proto\x1a\x1fgoogle/protobuf/timestamp.proto\"Y\n\x04Info\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\x0f\n\x07\x64\x65tails\x18\x02 \x01(\t\x12/\n\x0boccurred_at\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\"Z\n\x07\x46\x61ilure\x12\r\n\x05\x65rror\x18\x01 \x01(\t\x12\x0f\n\x07\x64\x65tails\x18\x02 \x01(\t\x12/\n\x0boccurred_at\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.Timestampb\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,])




_INFO = _descriptor.Descriptor(
  name='Info',
  full_name='Info',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='Info.message', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='details', full_name='Info.details', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='occurred_at', full_name='Info.occurred_at', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=52,
  serialized_end=141,
)


_FAILURE = _descriptor.Descriptor(
  name='Failure',
  full_name='Failure',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='error', full_name='Failure.error', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='details', full_name='Failure.details', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='occurred_at', full_name='Failure.occurred_at', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=143,
  serialized_end=233,
)

_INFO.fields_by_name['occurred_at'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_FAILURE.fields_by_name['occurred_at'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
DESCRIPTOR.message_types_by_name['Info'] = _INFO
DESCRIPTOR.message_types_by_name['Failure'] = _FAILURE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Info = _reflection.GeneratedProtocolMessageType('Info', (_message.Message,), {
  'DESCRIPTOR' : _INFO,
  '__module__' : 'responses_pb2'
  # @@protoc_insertion_point(class_scope:Info)
  })
_sym_db.RegisterMessage(Info)

Failure = _reflection.GeneratedProtocolMessageType('Failure', (_message.Message,), {
  'DESCRIPTOR' : _FAILURE,
  '__module__' : 'responses_pb2'
  # @@protoc_insertion_point(class_scope:Failure)
  })
_sym_db.RegisterMessage(Failure)


# @@protoc_insertion_point(module_scope)
