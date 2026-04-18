import datetime
from apps.domain.entities.base import Entity


class CategoryEntity(Entity):
    """
    类目
    """
    id: int
    name: str  # 名称
    show_index: int  # 展示序号
    extend_property: dict  # 属性信息
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: datetime.datetime

    def to_dict(self):
        base = {
            "id": self.id,
            "name": self.name,
        }
        return base
