from datetime import datetime, timedelta
from typing import Optional, List, Dict
from uuid import uuid4
Token_OUT = 3600*7


class UserToken:
    id: int
    uid: int
    token: str
    expired_at: datetime
    deleted_at: datetime

    def __init__(self, token: Optional[str] = None,
                 expired_at: Optional[datetime] = None, *args, **kwargs):
        _annotations_dict = getattr(self, "__annotations__")
        for kwarg, value in kwargs.items():
            if kwarg in _annotations_dict:
                setattr(self, kwarg, value)
        self.token = token if token else str(uuid4())
        self.expired_at = expired_at if expired_at else datetime.now() + timedelta(seconds=Token_OUT)

    def is_valid(self):
        if self.expired_at > datetime.now():
            return True
        return False
