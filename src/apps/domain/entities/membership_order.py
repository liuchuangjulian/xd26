import datetime
from apps.domain.entities.order_base import OrderStatus, OrderBase



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
