from typing import Optional
from pydantic import BaseModel, Field, root_validator


class AddToCartParams(BaseModel):
    p_id: int = Field(..., description="p_id")


class DelFromCartParams(BaseModel):
    p_id: int = Field(..., description="p_id")


class CartChangeNumParams(BaseModel):
    p_id: int = Field(..., description="p_id")
    num: int = Field(..., description="dif为0时，num有效，为设置为的数字")
    dif: int = Field(..., description="-1或1时，则忽略num，变成+1，-1")
