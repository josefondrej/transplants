from typing import Optional


class DatabaseMixin:
    """Add model_class().save_to_db() and model_class.find_by_id(identifier)

    Args:
        model_class: Class to add the methods to
        collection: pymongo Collection to use for loading / saving the data
        id_name: Name of the key that stores the identifier
    """

    def save_to_db(self):
        cls = self.__class__
        cls.collection.insert_one(self.to_dict())

    def update_db(self, **kwargs):
        cls = self.__class__
        field_name, value = [(fn, v) for fn, v in kwargs.items()][0]
        cls.collection.update_one(filter={cls.id_name: getattr(self, cls.id_name)},
                                  update={"$set": {field_name: value}})

    @classmethod
    def find_by_id(cls, identifier: str) -> Optional["model_class"]:
        one = cls.collection.find_one({cls.id_name: identifier})
        if one is None:
            return

        one.pop("_id")
        return cls.from_dict(one)