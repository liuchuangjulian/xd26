# import datetime
# from typing import List
# from js_kits.fastapi_kits.entity_base import BaseEntity
#
#
# class Community(BaseEntity):
#     """
#     小区
#     """
#     # id: int
#     # province: str  # 省
#     # city: str  # 市
#     # district: str  # 区
#     # name: str  # 小区
#     # lon: float
#     # lat: float
#     # created_at: datetime.datetime
#     # updated_at: datetime.datetime
#     # deleted_at: datetime.datetime
#     #
#     # def __init__(self, id=None, province=None, city=None,
#     #              name=None, lon=None, lat=None, district=None,
#     #              created_at=None,
#     #              updated_at=None, deleted_at=None, *args, **kwargs):
#     #     super().__init__()
#     #     self.id = id
#     #     self.province = province
#     #     self.city = city
#     #     self.name = name
#     #     self.district = district
#     #     self.lon = lon
#     #     self.lat = lat
#     #     self.created_at = created_at
#     #     self.updated_at = updated_at
#     #     self.deleted_at = deleted_at
#     #
#     # def to_dict(self, is_in_black=False):
#     #     base = {
#     #         "id": self.id,
#     #         "name": self.name,
#     #         "province": self.province,
#     #         "city": self.city,
#     #         "district": self.district,
#     #         "lon": self.lon,
#     #         "lat": self.lat,
#     #     }
#     #     if is_in_black:
#     #         base["price"] = base["original_price"]
#     #     return base
