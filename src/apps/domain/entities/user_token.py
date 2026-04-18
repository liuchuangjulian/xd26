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
        super().__init__()
        self.token = token if token else str(uuid4())
        self.expired_at = expired_at if expired_at else datetime.now() + timedelta(seconds=Token_OUT)

    def is_valid(self):
        if self.expired_at > datetime.now():
            return True
        return False
