from pydantic import BaseModel, Field


class RedeemCardParams(BaseModel):
    card_number: str = Field(..., description="兑换卡卡号")
