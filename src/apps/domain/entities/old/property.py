import datetime
from typing import List
from js_kits.fastapi_kits.entity_base import BaseEntity


class PropertyEntity(BaseEntity):
    """
    顾客资产: 积分、余额、优惠券
    """
    id: int
    uid: int
    p_id: int  # 商品id
    count: int  # 商品数量
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: datetime.datetime

    def __init__(self, id=None, name=None, index=None,
                 describe=None, tips=None, sold=None, img=None, original_price=None,
                 price=None, units=None,
                 extend_property=None,  created_at=None,
                 updated_at=None, deleted_at=None, *args, **kwargs):
        super().__init__()
        self.id = id
        self.describe = describe
        self.tips = tips
        self.sold = sold
        self.img = img
        self.original_price = original_price
        self.price = price
        self.units = units
        self.extend_property = extend_property
        self.name = name
        self.index = index
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

    def to_dict(self, is_in_black=False):
        base = {
            "id": self.id,
            "name": self.name,
            "describe": self.describe,
            "tips": self.tips,
            "sold": self.sold,
            "img": self.img,
            "original_price": self.original_price,
            "price": self.price,
            "units": self.units,
            "index": self.index,
        }
        if is_in_black:
            base["price"] = base["original_price"]
        return base
