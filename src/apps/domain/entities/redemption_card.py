from datetime import datetime, date
from typing import Optional
from decimal import Decimal
from js_kits.fastapi_kits.entity_base import Entity


class RedemptionCard(Entity):
    id: Optional[int]
    card_number: str
    amount: Decimal
    status: int
    expired_at: Optional[datetime]
    used_at: Optional[datetime]
    used_by: Optional[int]
    deleted_at: Optional[datetime]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    def to_dict(self):
        return {
            "id": self.id,
            "card_number": self.card_number,
            "amount": float(self.amount),
            "status": self.status,
            "expired_at": self.expired_at.strftime("%Y-%m-%d %H:%M:%S") if self.expired_at else None,
            "used_at": self.used_at.strftime("%Y-%m-%d %H:%M:%S") if self.used_at else None,
            "used_by": self.used_by,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
        }

    def is_valid(self):
        """检查兑换卡是否有效"""
        if self.status == 1:
            return False, "该兑换卡已使用"
        if self.status == 2:
            return False, "该兑换卡已失效"
        if self.expired_at and self.expired_at < datetime.now():
            return False, "该兑换卡已过期"
        return True, None

    def mark_as_used(self, uid):
        """标记为已使用"""
        self.status = 1
        self.used_at = datetime.now()
        self.used_by = uid
