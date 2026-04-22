import enum
from apps.domain.entities.base import Entity
from sqlalchemy import DateTime
from sqlalchemy.orm.attributes import flag_modified

type_map = {
    "recharge": "充值",
    "user_pay": "自助付款",
    "consume": "余额消费",
    "offline": "线下消费",
    "coin": "积分",
    "redemption": "兑换卡兑换"
}


class RecordType(enum.Enum):
    Recharge = "recharge"  # 充值
    Purchase = "purchase"  # 购买
    OfflineRecharge = "offline_recharge"  # 线下充值
    Coin = "coin"  # 积分兑换
    Redemption = "redemption"  # 兑换卡兑换


class RecordStatus(enum.Enum):
    UnPay = "un_pay"  # 充值未支付
    Paid = "paid"  # 充值已经支付
    AmountError = "amount_error"  # 支付金额与约定金额不一致
    Ok = "ok"


class TransferRecord(Entity):
    # 流通记录
    id: int  # 主键
    type: str  # 记录类型 余额消费、线下消费、充值、积分消费
    uid: int  # 用户id
    amount: int  # 交易金额 单位分
    amount_real: int  # 实际金额 单位分
    amount_gift: int  # 赠送金额 单位分
    amount_coin_count: int  # 积分
    op_uid: int  # 操作用户id，自己或者工作人员
    status: str  # 状态
    extra: dict  # 附加属性
    created_at: DateTime  # 创建时间

    def paid(self, amount):
        if amount == self.amount_real:
            self.status = RecordStatus.Paid.value
        else:
            self.status = RecordStatus.AmountError.value

    # def set_default(self, type):
    #     if type == "weixin_pay":
    #         self.status = RecordStatus.Paid.value
    #         self.type = RecordType.Recharge.value
    #         self.real = 0
    #         self.gift = 0
    #         self.coin_count = 0
    #         self.op_user_id = ""

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "status": self.status,
            "type_cn": type_map.get(self.type),
            "amount": f"{self.amount/100:.2f}",
            "amount_real": f"{self.amount_real/100:.2f}",
            "amount_gift": f"{self.amount_gift/100:.2f}",
            "amount_coin_count": self.amount_coin_count,
            "created_at": str(self.created_at),
        }

    def set_modified(self):
        flag_modified(self, "extra")

    def record_add_to_user_time(self):
        # 记录增加到用户上的次数
        if not hasattr(self, "extra"):
            self.extra = {}
        self.extra["add_time"] = self.extra.get("add_time", 0) + 1

    def is_add_to_user(self):
        # 是否没有增加到用户余额上（防止一笔记录，增加到用户身上多次）
        if not hasattr(self, "extra"):
            self.extra = {}
        return self.extra.get("add_time", 0) > 0
