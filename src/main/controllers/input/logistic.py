from pydantic import BaseModel, Field, root_validator


class QueryLogisticParams(BaseModel):
    order_id: int = Field(..., description="订单id")
