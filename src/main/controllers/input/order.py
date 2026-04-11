from typing import Optional, List
from pydantic import BaseModel, Field, root_validator

from apps.domain.entities.order import OrderStatus


class ProductCountParams(BaseModel):
    p_id: int = Field(..., description="产品id")
    count: int = Field(..., description="数量")


class CreateOrderParams(BaseModel):
    address_id: int = Field(..., description="地址id")
    coupon_id: int = Field(..., description="优惠券id")
    p_id_count_list: List[ProductCountParams] = Field(..., description="产品id列表")


class PreCreateOrderParams(BaseModel):
    coupon_id: int = Field(0, description="优惠券id，0表示自动选择最优优惠券")
    p_id_count_list: List[ProductCountParams] = Field(..., description="产品id列表")


class QueryOrderParams(BaseModel):
    status: int = Field(..., description="订单状态")


class QueryOrderLineParams(BaseModel):
    order_id: str = Field(..., description="order_id")


class ChangeOrderStatsParams(BaseModel):
    status: int = Field(..., description="订单状态")
    order_id: int = Field(..., description="order_id")

    @root_validator(allow_reuse=True, skip_on_failure=True)
    def check(cls, values):
        status = values.get("status")
        if status not in OrderStatus.user_can_changed_to():
            raise ValueError("状态非法")
        return values
