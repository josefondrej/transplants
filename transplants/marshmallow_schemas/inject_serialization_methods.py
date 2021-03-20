from typing import Dict


def inject_serialization_methods(model_class: type, schema_class: type):
    schema_instance = schema_class()

    def to_dict(self) -> Dict:
        return schema_instance.dump(self)

    def from_dict(cls, dictionary: Dict):
        return schema_instance.load(dictionary)

    model_class.to_dict = to_dict
    model_class.from_dict = classmethod(from_dict)
