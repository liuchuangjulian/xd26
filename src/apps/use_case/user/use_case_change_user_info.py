import logging
from js_kits.except_kits.except_kits import FastapiResult, ClientError
from apps.domain.repo.repo_coupons import CouponsRepository
from apps.domain.repo.repo_user import UserRepository

logger = logging.getLogger(__name__)


class UseCaseChangeUserInfo:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    async def execute(self, uid, **kwargs) -> None:
        async with self.repo.session as session:
            _, obj_list = await self.repo.get_list(session, equal_maps={"id": uid}, with_total=False)
            if not obj_list:
                raise ClientError({"msg": "用户不存在"})
            user_obj = obj_list[0]
            user_obj.update_value(**kwargs)
            await self.repo.add(session, user_obj)
            raise FastapiResult({"msg": "ok",
                                 "data": user_obj.user_info_to_dict()
                                 })
