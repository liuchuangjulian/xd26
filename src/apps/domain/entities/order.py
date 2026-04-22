import datetime
from typing import List
from apps.domain.entities.order_base import OrderStatus, OrderBase


class OrderEntity(OrderBase):
    """
    订单
    """
    id: int
    main_info: str  # 主要信息，用于展示
    uid: int
    real_pay: int  # 实际支付
    total: int  # 总金额
    count: int  # 总件数
    discount: int  # 总折扣
    status: int  # 状态：OrderStatus
    balance: int  # 余额
    coins: int  # 使用积分
    coupon_id_list: List[dict]  # 优惠券
    feedback_coins: int  # 回馈积分
    payment_id_list: List[int]  # 支付id列表
    delivery_id_list: List[int]  # 配送id列表
    # 微信支付相关字段
    out_trade_no: str  # 商户订单号
    transaction_id: str  # 微信支付订单号
    pay_time: datetime.datetime  # 支付时间
    extend_property: dict
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: datetime.datetime

    def refresh_data_from_ol(self, ol_list):
        self.count = sum([ol.count for ol in ol_list])
        self.total = sum([ol.amount for ol in ol_list])

        self.main_info = ",".join([ol.name for ol in ol_list[:2]]) + f"等{self.count}件商品"

    def set_address_obj(self, address_obj):
        # 地址信息放在订单里面，如果外面地址修改，不影响订单本身
        if not isinstance(self.extend_property, dict):
            self.extend_property = {}
        self.extend_property["address"] = address_obj.to_dict()

    def set_coupon_obj(self, coupon_obj):
        # 地址信息放在订单里面，如果外面地址修改，不影响订单本身
        if coupon_obj and coupon_obj.can_use(self.total):
            self.coupon_id_list.append(coupon_obj.to_dict())
            self.discount = sum([coupon["price"] for coupon in self.coupon_id_list])

    def description(self):
        return self.main_info

    @staticmethod
    def generate_out_trade_no():
        """生成商户订单号 - 购物订单使用 SHOP 前缀"""
        from random import sample
        from string import digits
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        random_str = ''.join(sample(digits, 6))
        return f"SHOP{timestamp}{random_str}"

    def mark_as_paid(self, transaction_id: str):
        """标记订单为已支付"""
        self.status = OrderStatus.Payed.value
        self.transaction_id = transaction_id
        self.pay_time = datetime.datetime.now()
        self.real_pay = self.total - self.discount
