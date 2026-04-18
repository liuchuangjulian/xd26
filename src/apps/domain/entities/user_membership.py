import datetime
from apps.domain.entities.base import Entity


class UserMembershipEntity(Entity):
    """
    用户开通会员信息
    """
    id: int
    uid: int
    membership_id: int
    membership_info: dict  # 快照
    start_day: datetime.date
    end_day: datetime.date
    extend_property: dict  # 扩展数据
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: datetime.datetime
