import datetime
from js_kits.fastapi_kits.enum_base import EnumDescriptions
from apps.domain.entities.base import Entity
from random import sample
from string import ascii_letters, digits

class OrderStatus(EnumDescriptions):
    # 已下单、已支付、已出库、已签收、已售后（部分退款、退货退款）
    Ordered = 1  # 已下单-未支付
    Paid = 2  # 已支付 【付款方式有不同：即有货到付款的‘支付’方式】
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
                OrderStatus.Paid.value,
                OrderStatus.Confirmed.value,
                OrderStatus.OutStocked.value,]

    @staticmethod
    def user_can_changed_to():
        return [OrderStatus.UserCancelled.value,
               ]


class OrderBase(Entity):
    pay_time: datetime.datetime  # 支付时间
    extend_property: dict
    status: int  # 状态：OrderStatus
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: datetime.datetime

    def paid_from_wx(self, resource):
        self.status = OrderStatus.Paid.value
        self.pay_time = datetime.datetime.now()
        if not isinstance(self.extend_property, dict):
            self.extend_property = {}
        self.extend_property["wx_resource"] = resource

    @staticmethod
    def _generate_out_trade_no():
        """生成商户订单号"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        random_str = ''.join(sample(digits, 6))
        return f"MEM{timestamp}{random_str}"
