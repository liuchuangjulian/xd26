import datetime
from typing import List
from js_kits.fastapi_kits.entity_base import BaseEntity


class Suggestion(BaseEntity):
    """
    反馈建议
    """
    id: int
    uid: int  # 订单id
    title: str  # 标题
    content: str  # 内容
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: datetime.datetime
