from pydantic import BaseModel
from typing import Optional
from main.controllers.pydantic_base.auto_title_field import AutoTitleField


class LoginResponseData(BaseModel):
    token: str = AutoTitleField(..., description="用户token")
    code: str = AutoTitleField(..., description="用户code")
    nickname: str = AutoTitleField(..., description="用户昵称")


class LoginResponse(BaseModel):
    code: int = AutoTitleField(..., description="状态码")
    msg: str = AutoTitleField(..., description="信息")
    data: LoginResponseData = AutoTitleField(..., description="登录数据")


class UserInfoData(BaseModel):
    avatar: str = AutoTitleField(..., description="用户头像")
    nickname: str = AutoTitleField(..., description="用户昵称")
    birthday: str = AutoTitleField(..., description="用户生日")
    code: str = AutoTitleField(..., description="会员号")
    wechat_id: str = AutoTitleField(..., description="微信ID")
    is_member: bool = AutoTitleField(..., description="是否是会员")


class UserInfoResponse(BaseModel):
    code: int = AutoTitleField(..., description="状态码")
    msg: str = AutoTitleField(..., description="信息")
    data: UserInfoData = AutoTitleField(..., description="用户信息")


class ChangeUserInfoResponse(BaseModel):
    code: int = AutoTitleField(..., description="状态码")
    msg: str = AutoTitleField(..., description="信息")
    data: Optional[UserInfoData] = AutoTitleField(None, description="修改结果")


class AvatarUploadData(BaseModel):
    url: str = AutoTitleField(..., description="头像URL")


class AvatarUploadResponse(BaseModel):
    code: int = AutoTitleField(..., description="状态码")
    msg: str = AutoTitleField(..., description="信息")
    data: AvatarUploadData = AutoTitleField(..., description="上传结果")
