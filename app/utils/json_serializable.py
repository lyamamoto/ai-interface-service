class JSONSerializable:
    def to_json(self):
        data = {}
        for attr_name in dir(self):
            if not attr_name.startswith("__") and not callable(getattr(self, attr_name)):
                attr_value = getattr(self, attr_name)
                if hasattr(attr_value, 'to_json'):  # Check if it's an instance of JSONSerializable
                    data[attr_name] = attr_value.to_json()
                else:
                    data[attr_name] = attr_value
        return data

    @classmethod
    def from_json(cls, json_data):
        instance = cls.__new__(cls)
        for attr_name, attr_value in json_data.items():
            if hasattr(attr_value, 'from_json'):  # Check if it's an instance of JSONSerializable
                setattr(instance, attr_name, attr_value.from_json(attr_value))
            else:
                setattr(instance, attr_name, attr_value)
        return instance

def JSONMapping(field_name):
    def decorator(func):
        setattr(func, '_json_mapping', field_name)
        return func
    return decorator