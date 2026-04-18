import logging
import random
from js_kits.except_kits.except_kits import FastapiResult, ClientError
from apps.domain.entities.config import ConfigEntity
from apps.domain.repo.repo_user import UserRepository

logger = logging.getLogger(__name__)


class QueryUserInfo:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def query(self, uid) -> None:
        async with self.repo.session as session:
            _, obj_list = await self.repo.get_list(session, equal_maps={"id": uid}, with_total=False)
            if not obj_list:
                raise ClientError({"msg": "用户不存在"})
            user_obj = obj_list[0]

            user_info = user_obj.user_info_to_dict()
            user_info["wechat_id"] = "暂无信息"

            _, config_obj_list = await self.repo.get_list(session, Entity=ConfigEntity, equal_maps={"key": "weixin_kf"}, with_total=False)
            if config_obj_list:
                config_obj = config_obj_list[0]
                try:
                    user_info["wechat_id"] = random.choice(config_obj.extend_property.get("wechat_id_list"))
                except Exception as e:
                    ...

            raise FastapiResult({"msg": "ok",
                                 "data": user_info
                                 })
