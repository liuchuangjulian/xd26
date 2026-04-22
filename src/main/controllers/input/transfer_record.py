from pydantic import BaseModel, Field


class QueryTransferRecordParams(BaseModel):
    status: str = Field("", description="状态筛选 (paid, un_pay 等)")
    type: str = Field("", description="类型筛选 (recharge, redemption, coin 等)")
