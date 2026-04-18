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
    max_purchase_count: int  # 最大购买数量
    extend_property: dict  # 扩展数据
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: datetime.datetime
