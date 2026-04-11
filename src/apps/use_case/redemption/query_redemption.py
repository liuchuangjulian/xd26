import logging
from js_kits.except_kits.except_kits import FastapiResult
from apps.domain.repo.repo_redemption import RedemptionRepository

logger = logging.getLogger(__name__)


class QueryRedemptionHistory:
    def __init__(self, repo: RedemptionRepository):
        self.repo = repo

    async def query(self, uid, page=1, page_size=10) -> None:
        """查询用户的兑换记录"""
        async with self.repo.session as session:
            # 查询用户的兑换记录，按兑换时间倒序
            total, obj_list = await self.repo.get_list(
                session,
                equal_maps={"uid": uid},
                page=page,
                page_size=page_size,
                order_by_list=["redemption_time DESC"]
            )

            raise FastapiResult({
                "msg": "ok",
                "total": total,
                "page": page,
                "page_size": page_size,
                "data": [obj.to_dict() for obj in obj_list]
            })
