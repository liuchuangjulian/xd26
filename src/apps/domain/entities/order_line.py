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

    def __init__(self, id=None, name=None, index=None, barcode=None, uid=None,
                 order_id=None, p_id=None, count=None, price=None, amount=None,
                 extend_property=None,  created_at=None,
                 updated_at=None, deleted_at=None, *args, **kwargs):
        super().__init__()
        self.id = id
        self.uid = uid
        self.order_id = order_id
        self.p_id = p_id
        self.count = count
        self.price = price
        self.extend_property = extend_property
        self.name = name
        self.barcode = barcode
        self.index = index
        self.amount = amount if amount else self.price * self.count
        self.created_at = created_at
        self.updated_at = updated_at
        self.deleted_at = deleted_at

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
