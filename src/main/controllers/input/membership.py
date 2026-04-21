from typing import Optional, List
from pydantic import BaseModel, Field, root_validator


class CreateUserMembershipParams(BaseModel):
    membership_id: int = Field(..., description="会员ID")


class QueryMembershipOrderParams(BaseModel):
    out_trade_no: Optional[str] = Field(None, description="商户订单号")
    status: Optional[int] = Field(None, description="订单状态")
