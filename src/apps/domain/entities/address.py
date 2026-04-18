import datetime
from apps.domain.entities.base import Entity

class Address(Entity):
    """
    地址
    """
    id: int
    selected: int  # 已选择
    uid: int
    province: str  # 省
    city: str  # 市
    district: str  # 区
    community_name: str  # 海螺花园
    building_unit_room: str  # 门牌地址，如：2号楼 1单元 2013室
    phone: str  # 手机
    name: str  # 联系人
    tag: str  # 家/公司/等
    created_at: datetime.datetime
    updated_at: datetime.datetime
    deleted_at: datetime.datetime

    # def __init__(self, *args, **kwargs):
    #     _annotations_dict = getattr(self, "__annotations__")
    #     for kwarg, value in kwargs.items():
    #         if kwarg in _annotations_dict:
    #             setattr(self, kwarg, value)

    def to_dict(self):
        base = {
            "id": self.id,
            "province": self.province,
            "city": self.city,
            "district": self.district,
            "name": self.name,
            "uid": self.uid,
            "community_name": self.community_name,
            "building_unit_room": self.building_unit_room,
            "selected": self.selected,
            "phone": self.phone,
            "tag": self.tag,
        }
        return base

    def update_all(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self, k):
                setattr(self, k, v)
