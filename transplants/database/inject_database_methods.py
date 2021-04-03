from typing import Optional

from pymongo.collection import Collection


def inject_database_methods(model_class: type, collection: Collection, id_name: str):
    """Add model_class().save_to_db() and model_class.find_by_id(identifier)

    Args:
        model_class: Class to add the methods to
        collection: pymongo Collection to use for loading / saving the data
        id_name: Name of the key that stores the identifier
    """

    def save_to_db(self):
        collection.insert_one(self.to_dict())

    def find_by_id(cls, identifier: str) -> Optional["model_class"]:
        one = collection.find_one({id_name: identifier})
        if one is None:
            return

        one.pop("_id")
        return model_class.from_dict(one)

    def update_db(self, **kwargs):
        field_name, value = [(fn, v) for fn, v in kwargs.items()][0]
        collection.update_one(filter={id_name: getattr(self, id_name)}, update={"$set": {field_name: value}})

    model_class.save_to_db = save_to_db
    model_class.update_db = update_db
    model_class.find_by_id = classmethod(find_by_id)
