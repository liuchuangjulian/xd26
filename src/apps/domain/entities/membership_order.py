import datetime
from apps.domain.entities.order_base import OrderStatus, OrderBase
from apps.domain.entities.user_membership import UserMembershipEntity
from random import sample
from string import digits


class MembershipOrderEntity(OrderBase):
    """
    会员购买订单
    """
    id: int
    uid: int  # 用户ID
    membership_id: int  # 会员类型ID
    out_trade_no: str  # 商户订单号
    transaction_id: str  # 微信支付订单号
    total_fee: int  # 订单金额（分）
    status: int  # 订单状态：MembershipOrderStatus
    membership_info: dict  # 会员信息快照
    pay_time: datetime.datetime  # 支付时间
    extend_property: dict  # 扩展数据
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: datetime.datetime

    def create_order(self, uid, membership):
        self.uid = uid
        self.membership_id = membership.id
        self.out_trade_no = self._generate_out_trade_no()
        self.status = OrderStatus.Ordered.value
        self.membership_info = membership.to_dict()
        self.total_fee = int(membership.price * 100)
        return self

    def mark_as_paid(self, transaction_id: str):
        """标记订单为已支付"""
        self.status = OrderStatus.Paid.value
        self.transaction_id = transaction_id
        self.pay_time = datetime.datetime.now()

    def create_membership(self, existing_memberships=None):
        """创建用户会员记录"""
        start_day = datetime.date.today()
        duration = self.membership_info.get("duration", 0)
        end_day = start_day + datetime.timedelta(days=duration)

        if existing_memberships:
            latest_membership = max(existing_memberships, key=lambda x: x.end_day)
            if latest_membership.end_day >= start_day:
                start_day = latest_membership.end_day
                end_day = start_day + datetime.timedelta(days=duration)
        return UserMembershipEntity(uid=self.uid,
                                   membership_id=self.membership_id,
                                   membership_info=self.membership_info,
                                   start_day=start_day, end_day=end_day,
                                   extend_property={"order_id": self.id},
                                   )

    # def to_dict(self):
    #     return {
    #         "id": self.id,
    #         "uid": self.uid,
    #         "membership_id": self.membership_id,
    #         "out_trade_no": self.out_trade_no,
    #         "transaction_id": self.transaction_id,
    #         "total_fee": self.total_fee,
    #         "status": self.status,
    #         "membership_info": self.membership_info,
    #         "pay_time": str(self.pay_time) if self.pay_time else None,
    #         "created_at": str(self.created_at),
    #     }
