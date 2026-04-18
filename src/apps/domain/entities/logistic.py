import datetime
from apps.domain.entities.base import Entity


class LogisticStatus:
    Picking = 1  # 拣货中
    ToBeShipped = 2  # 待出库
    Delivery = 3  # 派送中
    Received = 4  # 已收货
    ReInStorage = 5  # 退货入库
    PartScrapped = 6  # 部分货物损坏
    AllScrapped = 7  # 全部货物损坏


class Logistic(Entity):
    """
    物流
    """
    id: int
    order_id: int  # 订单id
    nodes: list  # 节点
    # {"name": "拣货中", "owner": "拣货员：xxx", "time": "2025-10-10 10:10:10", "phone": "021-12345678", "notes": ""}
    # {"name": "待出库", "owner": "出库员：xxx", "time": "2025-10-10 10:10:10", "phone": "021-12345678", "notes": ""}
    # {"name": "派送中", "owner": "派送员：xxx", "time": "2025-10-10 10:10:10", "phone": "021-12345678", "notes": ""}
    # {"name": "已收货", "owner": "派送员：xxx", "time": "2025-10-10 10:10:10", "phone": "021-12345678", "notes": ""}
    status: int  # 当前状态
    address_id: int  # 原始送货地址
    address_info: dict  # 地址快照
    created_at: datetime.datetime
    updated_at: datetime.datetime

    # def __init__(self, *args, **kwargs):
    #     _annotations_dict = getattr(self, "__annotations__")
    #     for kwarg, value in kwargs.items():
    #         if kwarg in _annotations_dict:
    #             setattr(self, kwarg, value)
        # self.coupon_id_list = self.coupon_id_list if self.coupon_id_list else []
        # self.payment_id_list = self.payment_id_list if self.payment_id_list else []
        # self.delivery_id_list = self.delivery_id_list if self.delivery_id_list else []
        # self.status = self.status if self.status else OrderStatus.Ordered.value

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
        return result_map
