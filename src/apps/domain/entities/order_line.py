import datetime
from apps.domain.entities.base import Entity


class OrderLineEntity(Entity):
    """
    订单行
    """
    id: int
    index: int
    barcode: str
    order_id: int
    uid: int   # 冗余
    name: str  # 产品名称
    p_id: int  # 商品id
    count: int  # 商品数量
    price: int  # 价格(单价格)
    amount: int   # 总价格
    extend_property: dict
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: datetime.datetime

    def build_from_product(self, p_obj, count):
        self.barcode = p_obj.barcode
        self.p_id = p_obj.id
        self.name = p_obj.name
        self.count = count
        self.price = p_obj.price
        self.amount = self.count * self.price
        return self

    def to_dict(self):
        base = {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "index": self.index,
        }
        # if is_in_black:
        #     base["price"] = base["original_price"]
        return base
