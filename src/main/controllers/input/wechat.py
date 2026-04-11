from datetime import date
from pydantic import BaseModel, Field, root_validator


class WechatLoginParams(BaseModel):
    code: str = Field(..., description="微信code")


class UserParams(BaseModel):
    nickname: str = Field(..., description="昵称")
    avatar: str = Field(..., description="头像")
    birthday: date = Field(..., description="生日")
