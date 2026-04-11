from pydantic import BaseModel
from main.controllers.pydantic_base.auto_title_field import AutoTitleField



class NoticeModel(BaseModel):
    show: int = AutoTitleField(..., description="是否显示通知，0-不显示，1-显示")
    title: str = AutoTitleField(None, description="通知标题")
    content: str = AutoTitleField(None, description="通知内容")


class NoticeResponse(BaseModel):
    code: int = AutoTitleField(..., description="状态码")
    msg: str = AutoTitleField(..., description="信息")
    data: NoticeModel = AutoTitleField(..., description="数据")
