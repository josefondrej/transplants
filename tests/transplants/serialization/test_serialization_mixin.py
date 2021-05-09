from unittest import TestCase

from marshmallow import fields

from transplants.serialization.serialization_mixin import SerializationMixin, add_marshmallow_schema, \
    serializable_property


class TestSerializationMixin(TestCase):
    def test_add_marshmallow_schema(self):
        @add_marshmallow_schema
        class Foo(SerializationMixin):
            def __init__(self, first_property: int, second_property: int = None):
                self._first = first_property
                self._second = second_property

            @serializable_property(fields.String(), serialize_name="frs_prp")
            def first_property(self):
                return self._first

            @property
            def second_property(self):
                return self._second

        foo = Foo(first_property="123")
        foo_serialized = foo.to_dict()
        self.assertDictEqual(foo_serialized, {"frs_prp": "123"})

        foo_deserialized = Foo.from_dict(foo_serialized)
        self.assertEqual(foo_deserialized.first_property, "123")
