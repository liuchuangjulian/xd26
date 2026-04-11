from pydantic import BaseModel, Field, root_validator


class PayParams(BaseModel):
    token: str = Field(..., description="token")
    amount: str = Field(..., description="金额")


# def prepare_recharge_input(params: PayParams, user_obj: User):
#     amount = int(float(params.amount)*100)
#     return RechargeInputDto(amount=amount, user_obj=user_obj)

class GetRecordParams(BaseModel):
    # token: str = Field(..., description="token")
    record_id: str = Field(..., description="out_trade_no")