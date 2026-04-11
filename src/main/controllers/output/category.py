from pydantic import BaseModel
from typing import List, Optional
from main.controllers.pydantic_base.auto_title_field import AutoTitleField


class CategoryItem(BaseModel):
    id: int = AutoTitleField(..., description="类别ID")
    name: str = AutoTitleField(..., description="类别名称")


class CategoryListResponse(BaseModel):
    code: int = AutoTitleField(..., description="状态码")
    msg: str = AutoTitleField(..., description="信息")
    data: List[CategoryItem] = AutoTitleField(..., description="类别列表")