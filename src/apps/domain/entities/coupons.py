import datetime
from js_kits.fastapi_kits.enum_base import EnumDescriptions
from apps.domain.entities.base import Entity


class CouponType(EnumDescriptions):
    NoneType = 0  # 无优惠券，方便计算
    SpendOff = 1  # 满减: 满6减去6
    SpendOffPer = 2  # 满打折: 满100打99折


class CouponGeneratedType(EnumDescriptions):
    ExperienceVip = 1
    Vip = 2
    SVip = 3

    @staticmethod
    def map() -> dict:
        return {
            CouponGeneratedType.ExperienceVip.value: "体验会员卡赠送",
            CouponGeneratedType.Vip.value: "会员卡赠送",
            CouponGeneratedType.SVip.value: "大会员卡赠送",
        }

    @property
    def description(self) -> str:
        return {
            self.ExperienceVip: "体验会员卡赠送",
            self.Vip: "会员卡赠送",
            self.SVip: "大会员卡赠送",
        }.get(self, "未知")


class Coupon(Entity):
    """
    优惠券
    """
    id: int
    coupon_type: int  # 优惠券类型：1  满减/满打折等
    generated_type: int  # 产生的类型：1 体验会员卡赠送
    title: str  # 运费优惠券
    price: int  # 面额，600，单位份
    limit: int  # 满多少才可使用，-1表示没有限制
    uid: int  # -1为所有人同时拥有
    extend_property: dict
    effected_at: datetime.date  # 生效日期
    expired_at: datetime.date  # 过期日期
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: datetime.datetime


    def can_user_use(self, uid):
        if uid == self.uid or self.uid == -1:
            return True
        return False

    def get_none_coupon(self):
        self.price = 0
        self.limit = -1
        self.coupon_type = CouponType.NoneType.value
        return self

    def can_use(self, total):
        # 是否可以用
        if self.effected_at and self.expired_at and self.effected_at <= datetime.datetime.now().date() <= self.expired_at:
            if self.limit > 0:
                # 有限制金额，需要比它小
                if total > self.limit:
                    return True
            else:
                # 无金额限制
                return True
        return False

    def calc_discount(self, order_line_list):
        total = sum([p.amount for p in order_line_list])
        # 计算折扣金额 (total单位为分)
        if self.can_use(total):
            if self.coupon_type == CouponType.SpendOff.value:
                return self.price
        return 0

    def to_dict(self):
        result_map = {}
        for key, value in self.__dict__.items():
            if not key.startswith("_"):
                if isinstance(value, datetime.datetime):
                    result_map[key] = value.strftime('%Y-%m-%d %H:%M:%S')
                elif isinstance(value, datetime.date):
                    result_map[key] = value.strftime('%Y-%m-%d')
                else:
                    result_map[key] = value
        result_map["generated_type"] = CouponGeneratedType.map().get(self.generated_type)

        result_map["price_str"] = f"{self.price/100:.2f}"
        result_map["limit_str"] = f"{self.limit/100:.2f}" if self.limit > 0 else -1
        return result_map
