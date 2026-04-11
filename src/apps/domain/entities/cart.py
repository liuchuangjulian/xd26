import datetime


class CartEntity:
    """
    购物车
    """
    id: int
    uid: int
    p_id_info_map: dict  # {p_id: 数量}
    p_list: list  # [{p_id: xx, 数量: 1}]
    extend_property: dict
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: datetime.datetime

    def __init__(self, *args, **kwargs):
        _annotations_dict = getattr(self, "__annotations__")
        for kwarg, value in kwargs.items():
            if kwarg in _annotations_dict:
                setattr(self, kwarg, value)
        if self.p_id_info_map is None:
            self.p_id_info_map = {}
        if self.p_list is None:
            self.p_list = []
        if self.extend_property is None:
            self.extend_property = {}

    def get_p_ids(self):
        return [pid for pid, count in self.p_id_info_map.items() if count > 0]

    def init_and_add_one(self, uid, p_id):
        p_id = str(p_id)
        self.uid = uid
        self.add_one(p_id)
        return self

    def top_first(self, p_id):
        temp = [{"p_id": p_id, "count": self.p_id_info_map[p_id]}]
        for data in self.p_list:
            if data["p_id"] != p_id:
                temp.append(data)
        self.p_list = temp

    def add_one(self, p_id, limit_count=-1):
        p_id = str(p_id)
        if p_id not in self.p_id_info_map:
            self.p_id_info_map[p_id] = 0
        if not (0 < limit_count <= self.p_id_info_map[p_id]):
            self.p_id_info_map[p_id] += 1
        self.top_first(p_id)

    def set_count(self, p_id, count, limit_count, dif):
        p_id = str(p_id)
        if p_id not in self.p_id_info_map:
            self.p_id_info_map[p_id] = 0
        if dif:
            self.p_id_info_map[p_id] += dif
        else:
            if limit_count < 0:
                self.p_id_info_map[p_id] = count
            else:
                self.p_id_info_map[p_id] = limit_count if count > limit_count else count
        self.top_first(p_id)

    def add_to_order_to_delete(self, p_id_list):
        for p_id in p_id_list:
            if p_id in self.p_id_info_map:
                del self.p_id_info_map[p_id]
        temp = []
        for data in self.p_list:
            if data["p_id"] not in p_id_list:
                temp.append(data)
        self.p_list = temp

    def to_dict(self, product_map):
        base = []
        for p_dict in self.p_list:
            if p_dict["count"] < 1:
                continue
            temp = {
                    "p_id": int(p_dict["p_id"]),
                    "count": p_dict["count"],
                }
            temp.update(product_map[int(p_dict["p_id"])])
            base.append(temp)
        return base
