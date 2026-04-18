from datetime import datetime, timedelta
from typing import Optional, List, Dict
from uuid import uuid4
from apps.domain.entities.base import Entity

Token_OUT = 3600*7


class UserToken(Entity):
    id: int
    uid: int
    token: str
    expired_at: datetime
    deleted_at: Optional[datetime]

    def __init__(self, token: Optional[str] = None,
                 expired_at: Optional[datetime] = None, *args, **kwargs):
        # 先设置 token 和 expired_at
        if token:
            kwargs['token'] = token
        if expired_at:
            kwargs['expired_at'] = expired_at

        # 然后调用父类初始化，处理所有 kwargs（包括 uid）
        super().__init__(**kwargs)

        # 如果父类没有设置 token 和 expired_at，使用默认值
        if not getattr(self, 'token', None):
            self.token = str(uuid4())
        if not getattr(self, 'expired_at', None):
            self.expired_at = datetime.now() + timedelta(seconds=Token_OUT)

    def is_valid(self):
        if self.expired_at > datetime.now():
            return True
        return False
