from datetime import datetime, date
from typing import Optional
from decimal import Decimal
from apps.domain.entities.base import Entity



class RedemptionCard(Entity):
    """
    兑换卡
    """
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

    def do_record(self, uid):
        from apps.domain.entities.transfer_record import TransferRecord, RecordType, RecordStatus
        amount_cents = int(self.amount * 100)  # 转换为分
        return TransferRecord(type=RecordType.Redemption.value,
                                uid=uid,
                                amount=amount_cents,
                                amount_real=amount_cents,
                                amount_gift=0,
                                amount_coin_count=0,
                                op_uid=uid,
                                status=RecordStatus.Paid.value,
                                extra={
                                    "redemption_card_id": self.id,
                                    "card_number": self.card_number,
                                    "amount": float(self.amount)
                                    }
                                )


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
