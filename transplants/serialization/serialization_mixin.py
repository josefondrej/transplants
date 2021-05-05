from typing import Dict, Callable, Optional

from marshmallow import fields, Schema, post_load

_MARSHMALLOW_FIELD_TYPE_ATTRIBUTE_NAME = "__marshmallow_field_type__"
_SERIALIZE_NAME_ATTRIBUTE_NAME = "__serialize_as__"
_CLS_NAME_FIELD_NAME = "__cls_name__"


class _SerializableProperty(property):
    pass


def _set_marshmallow_field_type(obj: object, marshmallow_field_type: type):
    setattr(obj, _MARSHMALLOW_FIELD_TYPE_ATTRIBUTE_NAME, marshmallow_field_type)


def _set_serialize_name(obj: object, serialize_name: Optional[str] = None):
    setattr(obj, _SERIALIZE_NAME_ATTRIBUTE_NAME, serialize_name)


def _get_marshmallow_field_type(obj: object):
    return getattr(obj, _MARSHMALLOW_FIELD_TYPE_ATTRIBUTE_NAME, None)


def _get_serialize_name(obj: object):
    return getattr(obj, _SERIALIZE_NAME_ATTRIBUTE_NAME, None)


def _get_serializable_properties_with_marshmallow_types(cls):
    return {key: _get_marshmallow_field_type(getattr(cls, key))
            for key, value in cls.__dict__.items()
            if isinstance(value, _SerializableProperty)}


def _get_serializable_properties(cls) -> Dict[str, _SerializableProperty]:
    base_classes = cls.__bases__
    serializable_properties = {key: value for key, value in cls.__dict__.items() if
                               isinstance(value, _SerializableProperty)}

    if len(base_classes) > 0:
        for base_cls in base_classes:
            base_serializable_properties = _get_serializable_properties(base_cls)
            serializable_properties.update(base_serializable_properties)

    return serializable_properties


class _SchemaPreregisteredPostLoad(Schema):
    OBJECT_CLASS = None

    @post_load
    def make_obj(self, data, **kwargs):
        return self.OBJECT_CLASS._marshmallow_post_load(data)


def add_marshmallow_schema(cls):
    serializable_property_name_to_property = _get_serializable_properties(cls)
    serializable_property_names_to_marshmallow_types = dict()
    for prop_name, prop in serializable_property_name_to_property.items():
        schema_field_name = _get_serialize_name(prop) or prop_name
        schema_field_type = _get_marshmallow_field_type(prop)
        schema_field_type.attribute = prop_name
        serializable_property_names_to_marshmallow_types[schema_field_name] = schema_field_type

    marshmallow_schema = _SchemaPreregisteredPostLoad.from_dict(
        name=cls.__name__,
        fields=serializable_property_names_to_marshmallow_types
    )

    marshmallow_schema.OBJECT_CLASS = cls

    cls.marshmallow_schema = marshmallow_schema
    cls.marshmallow_schema_instance = cls.marshmallow_schema()

    return cls


def serializable_property(marshmallow_field_type: type, serialize_name: Optional[str] = None) -> Callable[
    [Callable], Callable]:
    def decorator(func: Callable) -> Callable:
        decorated_func = _SerializableProperty(func)
        _set_marshmallow_field_type(decorated_func, marshmallow_field_type)
        _set_serialize_name(decorated_func, serialize_name)
        return decorated_func

    return decorator


class SerializationMixin:
    def to_dict(self) -> Dict:
        return self.marshmallow_schema_instance.dump(self)

    @classmethod
    def from_dict(cls, dictionary: Dict) -> "SerializationMixin":
        model = cls.marshmallow_schema_instance.load(dictionary)
        return model

    @classmethod
    def _marshmallow_post_load(cls, data):
        return cls(**data)


if __name__ == '__main__':
    # TODO: Add to tests
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


    foo = Foo(first_property=123)
    dictionary = foo.to_dict()
    print(dictionary)

    foo_deserialized = Foo.from_dict(dictionary)
    print(foo_deserialized.first_property)
