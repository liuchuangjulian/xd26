import datetime
from typing import List
from js_kits.fastapi_kits.enum_base import EnumDescriptions


class OrderStatus(EnumDescriptions):
    # 已下单、已支付、已出库、已签收、已售后（部分退款、退货退款）
    Ordered = 1  # 已下单-未支付
    Payed = 2  # 已支付 【付款方式有不同：即有货到付款的‘支付’方式】
    Confirmed = 3  # 系统已确认【可以发货】
    OutStocked = 4  # 已出库
    Signed = 5  # 已签收：物流员定的
    UserConfirmed = 6  # 用户确认
    UserCancelled = 7  # 已取消
    SystemCancelled = 8  # 系统已取消
    Finished = 9  # 已结束
    Deleted = 10  # 已删除

    @staticmethod
    def user_can_changed():
        return [OrderStatus.Ordered.value,
                OrderStatus.Payed.value,
                OrderStatus.Confirmed.value,
                OrderStatus.OutStocked.value,]

    @staticmethod
    def user_can_changed_to():
        return [OrderStatus.UserCancelled.value,
               ]


class OrderEntity:
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
    extend_property: dict
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: datetime.datetime

    def __init__(self, *args, **kwargs):
        _annotations_dict = getattr(self, "__annotations__")
        for kwarg, value in kwargs.items():
            if kwarg in _annotations_dict:
                setattr(self, kwarg, value)
        self.coupon_id_list = self.coupon_id_list if self.coupon_id_list else []
        self.payment_id_list = self.payment_id_list if self.payment_id_list else []
        self.delivery_id_list = self.delivery_id_list if self.delivery_id_list else []
        self.status = self.status if self.status else OrderStatus.Ordered.value

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

    def to_dict(self):
        base = {
            "id": self.id,
            "main_info": self.main_info,
            "uid": self.uid,
            "real_pay": self.real_pay,
            "total": self.total,
            "count": self.count,
            "discount": self.discount,
            "status": self.status,
            "balance": self.balance,
            "coins": self.coins,
            "coupon_id_list": self.coupon_id_list,
            "feedback_coins": self.feedback_coins,
            "payment_id_list": self.payment_id_list,
            "delivery_id_list": self.delivery_id_list,
            "extend_property": self.extend_property,
        }
        return base
