import datetime
from typing import List
from apps.domain.entities.base import Entity


class ProductsEntity(Entity):
    """
    商品
    """
    id: int
    category_id_list: List[int]  #
    show_index: int  # 展示序号
    name: str  # 名称
    barcode: str
    describe: str  # 描述
    tips: List[str]
    sold: int  # 已卖出
    img: str  # 主图
    original_price: int  # 原价-价格
    price: int  # 售卖-价格
    units: str  # 单位
    extend_property: dict  # 属性信息
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: datetime.datetime

    def get_limit_count(self):
        # 限购数量
        if self.extend_property and "limit_count" in self.extend_property:
            return self.extend_property["limit_count"]
        return -1

    def to_dict(self, is_in_black=False):
        base = {
            "id": self.id,
            "name": self.name,
            "describe": self.describe,
            "tips": self.tips,
            "sold": self.sold,
            "img": self.img,
            "original_price": f"{self.original_price/100:.2f}",
            "price": f"{self.price/100:.2f}",
            "units": self.units,
            "show_index": self.show_index,
        }
        if is_in_black:
            base["price"] = base["original_price"]
        return base
