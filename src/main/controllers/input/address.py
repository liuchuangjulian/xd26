from typing import Optional, List
from pydantic import BaseModel, Field, root_validator


class CreateAddressParams(BaseModel):
    province: str = Field(..., description="省")
    city: str = Field(..., description="市")
    district: str = Field(..., description="区")
    community_name: str = Field(..., description="社区名")
    building_unit_room: str = Field("", description="栋")
    selected: int = Field(..., description="已选择")
    # unit: str = Field("", description="单元")
    # room: str = Field("", description="room")
    phone: str = Field(..., description="phone")
    name: str = Field("", description="name")
    tag: str = Field("", description="name")


class UpdateAddressParams(BaseModel):
    address_id: int = Field(..., description="address_id")
    province: str = Field(..., description="省")
    city: str = Field(..., description="市")
    district: str = Field(..., description="区")
    community_name: str = Field(..., description="社区名")
    building_unit_room: str = Field("", description="详细地址")
    selected: int = Field(..., description="已选择")
    # room: str = Field("", description="room")
    phone: str = Field(..., description="phone")
    name: str = Field("", description="name")
    tag: str = Field("", description="name")


class AddressListParams(BaseModel):
    selected: int = Field(0, description="selected")

class DeleteAddressParams(BaseModel):
    address_id: int = Field(..., description="address_id")
