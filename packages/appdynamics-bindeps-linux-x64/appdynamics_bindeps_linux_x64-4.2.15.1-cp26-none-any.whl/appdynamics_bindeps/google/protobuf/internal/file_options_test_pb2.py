# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/protobuf/internal/file_options_test.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from appdynamics_bindeps.google.protobuf import descriptor as _descriptor
from appdynamics_bindeps.google.protobuf import message as _message
from appdynamics_bindeps.google.protobuf import reflection as _reflection
from appdynamics_bindeps.google.protobuf import symbol_database as _symbol_database
from appdynamics_bindeps.google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from appdynamics_bindeps.google.protobuf import descriptor_pb2 as google_dot_protobuf_dot_descriptor__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/protobuf/internal/file_options_test.proto',
  package='google.protobuf.python.internal',
  syntax='proto2',
  serialized_pb=_b('\n0google/protobuf/internal/file_options_test.proto\x12\x1fgoogle.protobuf.python.internal\x1a google/protobuf/descriptor.proto\"\x1e\n\nFooOptions\x12\x10\n\x08\x66oo_name\x18\x01 \x01(\t:a\n\x0b\x66oo_options\x12\x1c.google.protobuf.FileOptions\x18\xac\xec\xb6\x39 \x01(\x0b\x32+.google.protobuf.python.internal.FooOptions')
  ,
  dependencies=[google_dot_protobuf_dot_descriptor__pb2.DESCRIPTOR,])
_sym_db.RegisterFileDescriptor(DESCRIPTOR)


FOO_OPTIONS_FIELD_NUMBER = 120436268
foo_options = _descriptor.FieldDescriptor(
  name='foo_options', full_name='google.protobuf.python.internal.foo_options', index=0,
  number=120436268, type=11, cpp_type=10, label=1,
  has_default_value=False, default_value=None,
  message_type=None, enum_type=None, containing_type=None,
  is_extension=True, extension_scope=None,
  options=None)


_FOOOPTIONS = _descriptor.Descriptor(
  name='FooOptions',
  full_name='google.protobuf.python.internal.FooOptions',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='foo_name', full_name='google.protobuf.python.internal.FooOptions.foo_name', index=0,
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
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=119,
  serialized_end=149,
)

DESCRIPTOR.message_types_by_name['FooOptions'] = _FOOOPTIONS
DESCRIPTOR.extensions_by_name['foo_options'] = foo_options

FooOptions = _reflection.GeneratedProtocolMessageType('FooOptions', (_message.Message,), dict(
  DESCRIPTOR = _FOOOPTIONS,
  __module__ = 'google.protobuf.internal.file_options_test_pb2'
  # @@protoc_insertion_point(class_scope:google.protobuf.python.internal.FooOptions)
  ))
_sym_db.RegisterMessage(FooOptions)

foo_options.message_type = _FOOOPTIONS
google_dot_protobuf_dot_descriptor__pb2.FileOptions.RegisterExtension(foo_options)

# @@protoc_insertion_point(module_scope)
