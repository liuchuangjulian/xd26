from pydantic import BaseModel
from typing import List, Optional
from main.controllers.pydantic_base.auto_title_field import AutoTitleField


class MembershipItem(BaseModel):
    id: int = AutoTitleField(..., description="会员ID")
    name: str = AutoTitleField(..., description="会员名称")
    price: float = AutoTitleField(..., description="价格")
    duration: int = AutoTitleField(..., description="有效期（天）")
    description: str = AutoTitleField(..., description="描述")
    status: int = AutoTitleField(..., description="状态：1-可用，0-不可用")
    max_purchase_count: int = AutoTitleField(..., description="最大购买数量，0表示无限制")
    purchased_count: int = AutoTitleField(..., description="已购买数量")


class MembershipListResponse(BaseModel):
    code: int = AutoTitleField(..., description="状态码")
    msg: str = AutoTitleField(..., description="信息")
    data: List[MembershipItem] = AutoTitleField(..., description="会员列表")


class CreateUserMembershipResponse(BaseModel):
    code: int = AutoTitleField(..., description="状态码")
    msg: str = AutoTitleField(..., description="信息")
    data: dict = AutoTitleField(..., description="开通结果")
