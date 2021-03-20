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

    def find_by_id(cls, identifier: str) -> "model_class":
        one = collection.find_one({id_name: identifier})
        one.pop("_id")
        return model_class.from_dict(one)

    model_class.save_to_db = save_to_db
    model_class.find_by_id = classmethod(find_by_id)
