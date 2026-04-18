import logging
import random
from datetime import date
from js_kits.except_kits.except_kits import FastapiResult, ClientError
from sqlalchemy import false
from apps.domain.entities.config import ConfigEntity
from apps.domain.repo.repo_user import UserRepository
from apps.domain.repo.repo_user_membership import UserMembershipRepository

logger = logging.getLogger(__name__)


class QueryUserInfo:
    def __init__(self, repo: UserRepository, user_membership_repo: UserMembershipRepository):
        self.repo = repo
        self.user_membership_repo = user_membership_repo

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

            # 查询用户当前是否有有效的会员
            _, user_membership_list = await self.user_membership_repo.get_list(
                session,
                equal_maps={"uid": uid},
                with_total=False
            )
            # 判断是否有任何会员记录的 end_day 大于等于今天
            today = date.today()
            is_member = false
            for user_membership in user_membership_list:
                if user_membership.start_day <= today <= user_membership.end_day:
                    is_member = True
            user_info["is_member"] = is_member
            raise FastapiResult({"msg": "ok",
                                 "data": user_info
                                 })
