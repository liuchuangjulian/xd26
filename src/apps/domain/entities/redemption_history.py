import datetime
from decimal import Decimal


class RedemptionHistory:
    id: int
    uid: int
    card_number: str
    card_password: str
    amount: Decimal
    status: int
    redemption_time: datetime.datetime
    expired_at: datetime.datetime
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: datetime.datetime

    def __init__(self, *args, **kwargs):
        _annotations_dict = getattr(self, "__annotations__")
        for kwarg, value in kwargs.items():
            if kwarg in _annotations_dict:
                setattr(self, kwarg, value)

    def to_dict(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "card_number": self.card_number,
            "amount": float(self.amount),
            "status": self.status,
            "redemption_time": self.redemption_time.strftime("%Y-%m-%d %H:%M:%S") if self.redemption_time else "",
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else ""
        }
