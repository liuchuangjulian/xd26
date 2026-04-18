import datetime
from apps.domain.entities.base import Entity


class Area(Entity):
    id: int
    code: str
    name: str
    parent_code: str
    level: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: datetime.datetime

    # def __init__(self, *args, **kwargs):
    #     _annotations_dict = getattr(self, "__annotations__")
    #     for kwarg, value in kwargs.items():
    #         if kwarg in _annotations_dict:
    #             setattr(self, kwarg, value)

    def to_dict(self):
        return {
            "code": getattr(self, "code", ""),
            "name": getattr(self, "name", ""),
            "parent_code": getattr(self, "parent_code", None),
            "level": getattr(self, "level", 0),
        }

    def to_tree_dict(self, children=None):
        return {
            "code": self.code,
            "name": self.name,
            "parent_code": self.parent_code,
            "level": self.level,
            "children": children if children else []
        }
