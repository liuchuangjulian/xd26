import json
import logging
import time
from apps.domain.entities.user import User
from apps.domain.entities.user_token import UserToken
from js_kits.except_kits.except_kits import FastapiResult, PureException, BackendException, ClientError, UnauthorizedError
import os
from js_kits.arequest.arequest import aio_request
from apps.domain.repo.repo_user import UserRepository

logger = logging.getLogger(__name__)


class WechatLoginUseCase:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def get_mp_openid(self, code):
        """
        """
        url = "https://api.weixin.qq.com/sns/jscode2session"
        params_dict = {
            "appid": os.getenv(f"MP_APPID"),
            "secret": os.getenv(f"MP_SECRET"),
            "js_code": code,
            "grant_type": "authorization_code"
        }
        t = time.time()
        status, data = await aio_request(url, params_dict=params_dict)
        total_time = time.time() - t
        params_dict["secret"] = f'*{params_dict["secret"][-2]}' if params_dict["secret"] else params_dict["secret"]
        logger.info(f"get_mp_openid url:{url},params_dict:{json.dumps(params_dict)},total_time:{total_time:.2f},"
                    f"status:{status},data:{json.dumps(data)}")
        if status != 200 or not isinstance(data, dict) or "errcode" in data:
            raise FastapiResult({"msg": "微信信息获取异常"})
        return data.get("unionid"), data.get("openid")

    async def execute(self, code) -> None:
        async with self.repo.session as session:
            # _, openid = await self.get_mp_openid(code)
            openid = "1111111111111111"
            _, user_obj_list = await self.repo.get_list(session, page_size=1, with_total=False,
                                                        equal_maps={"wechat_openid": openid})
            if user_obj_list:
                obj_user = user_obj_list[0]
            else:
                obj_user = User(wechat_openid=openid, deleted_at=None)
                obj_user.generate_code_nickname()
                await self.repo.add(session, obj_user)
            logger.info(f"obj_user.id: {obj_user.id}")
            user_token_obj = UserToken(uid=obj_user.id)
            await self.repo.add(session, user_token_obj)
            raise FastapiResult({"data": obj_user.to_login_result(user_token_obj.token)})
