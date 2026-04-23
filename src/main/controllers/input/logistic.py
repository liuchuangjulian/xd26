from typing import Optional
from pydantic import BaseModel, Field, root_validator


class QueryLogisticParams(BaseModel):
    order_id: int = Field(..., description="订单id")


class UpdateLogisticStatusParams(BaseModel):
    order_id: int = Field(..., description="订单id")
    status: int = Field(..., description="配送状态")
    node_name: str = Field(..., description="节点名称")
    owner: str = Field(..., description="负责人")
    phone: str = Field(..., description="联系电话")
    notes: str = Field("", description="备注")
