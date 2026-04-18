import datetime
from apps.domain.entities.base import Entity


class MembershipEntity(Entity):
    """
    可以开通的会员信息
    """
    id: int
    name: str  # 会员名称
    price: float  # 价格
    duration: int  # 有效期（天）
    description: str  # 描述
    status: int  # 状态：1-启用，0-禁用
    show_index: int  # 展示序号
    extend_property: dict  # 扩展数据
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: datetime.datetime

    def __init__(self, id=None, name=None, price=None, duration=None, description=None,
                 status=None, show_index=None, extend_property=None,
                 created_at=None, updated_at=None, deleted_at=None, *args, **kwargs):
        super().__init__()
        self.id = id
        self.name = name
        self.price = price
        self.duration = duration
        self.description = description
        self.status = status
        self.show_index = show_index
        self.extend_property = extend_property
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def to_dict(self):
        base = {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "status": self.status,
            "duration": self.duration,
            "description": self.description,
        }
        return base
