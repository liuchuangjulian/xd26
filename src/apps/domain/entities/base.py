from datetime import datetime, date
from decimal import Decimal


class Entity:
    def __init__(self, *args, **kwargs):
        _annotations_dict = getattr(self, "__annotations__")
        for attr_name, attr_type in _annotations_dict.items():
            if attr_name not in kwargs:
                if attr_type == int and attr_name != "id":
                    setattr(self, attr_name, 0)
                elif attr_type == float:
                    setattr(self, attr_name, 0.0)
                elif attr_type == str:
                    setattr(self, attr_name, "")
                elif attr_type == bool:
                    setattr(self, attr_name, False)
                elif attr_type == list:
                    setattr(self, attr_name, [])
                elif attr_type == dict:
                    setattr(self, attr_name, {})
                # elif attr_type == datetime:
                #     setattr(self, attr_name, datetime.now())
                # elif attr_type == date:
                #     setattr(self, attr_name, date.today())
                else:
                    setattr(self, attr_name, None)
        for kwarg, value in kwargs.items():
            if kwarg in _annotations_dict:
                setattr(self, kwarg, value)

    def to_dict(self, **kwargs):
        result_map = {}
        for key, value in self.__dict__.items():
            if not key.startswith("_"):
                if isinstance(value, datetime):
                    result_map[key] = value.strftime("%Y-%m-%d %H:%M:%S")
                elif isinstance(value, date):
                    result_map[key] = value.strftime("%Y-%m-%d")
                elif isinstance(value, Decimal):
                    result_map[key] = round(float(value), 2)
                else:
                    result_map[key] = value
        return result_map

    def delete(self):
        """标记为删除"""
        if hasattr(self, "deleted_at"):
            setattr(self, "deleted_at", datetime.now())
