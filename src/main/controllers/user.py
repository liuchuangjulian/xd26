from aioredis import Redis
from js_kits.except_kits.except_kits import FastapiResult, UnFoundError
from fastapi_injector import Injected
from fastapi import APIRouter, Request, UploadFile, Depends, Body
import logging
from js_kits.fastapi_kits.user_route import UserRoute
from apps.domain.repo.repo_user import UserRepository
from apps.use_case.user.query_user_info import QueryUserInfo
from apps.use_case.user.use_case_change_user_info import UseCaseChangeUserInfo
from apps.use_case.user.use_case_wechat_login import WechatLoginUseCase
from apps.file_upload import save_upload_file
from main.controllers.input.wechat import WechatLoginParams, UserParams
from main.controllers.output.user import LoginResponse, UserInfoResponse, ChangeUserInfoResponse, AvatarUploadResponse
from main.controllers.check_auth import auth

router_user = APIRouter(route_class=UserRoute, prefix="", tags=["user"])
logger = logging.getLogger(__name__)


@router_user.post("/login/mp", response_model=LoginResponse)
async def wechat_mp_login(params: WechatLoginParams = Body(...),
                          use_case: WechatLoginUseCase = Injected(WechatLoginUseCase)):
    # raise FastapiResult({"data": {
    #     "token": "7539b33b-a066-4dbc-b90c-f1f038fa429b",
    #     "code": "2332055158",
    #     "nickname": "会员23320-55158",
    # }})
    # 小程序登录
    await use_case.execute(params.code)
'''
 curl -X 'POST' \
  'http://localhost:8080/api/login/mp' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"code": "string"}' | jq .
'''


@router_user.get("/user/info", response_model=UserInfoResponse)
@auth
async def get_info(request: Request, redis_client: Redis = Injected(Redis),
                   user_repo: UserRepository = Injected(UserRepository), uid=None,
                   use_case: QueryUserInfo = Injected(QueryUserInfo)):
    await use_case.query(uid)
'''
curl -X 'GET' 'http://localhost:8080/api/user/info' -H 'token: 7539b33b-a066-4dbc-b90c-f1f038fa429b' | jq .
'''


# @router_user.post("/user", response_model=ChangeUserInfoResponse)
# @auth
# async def change_info(request: Request, redis_client: Redis = Injected(Redis),
#                       user_repo: UserRepository = Injected(UserRepository), uid=None, params: UserParams = Body(...),
#                       use_case: UseCaseChangeUserInfo = Injected(UseCaseChangeUserInfo)):
#     await use_case.execute(uid, **dict(params))
# '''
# curl -X 'POST' \
#   'http://localhost:8080/api/user' \
#   -H 'token: 7539b33b-a066-4dbc-b90c-f1f038fa429b'  \
#   -H 'Content-Type: application/json' \
#   -d '{"nickname": "新昵称",  "avatar": "新avatar",  "birthday": "2025-10-01"}' | jq .
# '''


@router_user.post("/user/avatar", response_model=AvatarUploadResponse)
@auth
async def upload_avatar(
    request: Request,
    file: UploadFile,
    redis_client: Redis = Injected(Redis),
    user_repo: UserRepository = Injected(UserRepository),
    uid=None,
):
    """上传用户头像"""
    # 保存文件
    file_url = await save_upload_file(
        file=file,
        user_id=uid,
        upload_dir="uploads/avatars"
    )
    # 更新数据库中的头像字段
    async with user_repo.session as session:
        _, obj_list = await user_repo.get_list(session, equal_maps={"id": uid}, with_total=False)
        if not obj_list:
            raise UnFoundError({"msg": "用户不存在"})
        user_obj = obj_list[0]
        user_obj.avatar = file_url
        await user_repo.add(session, user_obj)

    raise FastapiResult({
        "msg": "上传成功",
        "data": {"url": file_url}
    })

'''
# 上传头像
curl -X 'POST' \
  'http://localhost:8080/api/user/avatar' \
  -H 'token: 7539b33b-a066-4dbc-b90c-f1f038fa429b' \
  -H 'accept: application/json' \
  -F 'file=@/path/to/your/image.jpg' | jq .
'''