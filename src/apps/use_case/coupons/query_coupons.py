import logging
from js_kits.except_kits.except_kits import FastapiResult
from apps.domain.repo.repo_coupons import CouponsRepository

logger = logging.getLogger(__name__)


class QueryCoupons:
    def __init__(self, repo: CouponsRepository):
        self.repo = repo

    async def query(self, uid, page, page_size) -> None:
        async with self.repo.session as session:
            total, obj_list = await self.repo.get_list(session, equal_maps={"uid": uid}, page=page, page_size=page_size)
            raise FastapiResult({"msg": "ok",
                                 "total": total,
                                 "page": page,
                                 "page_size": page_size,
                                 "data": [obj.to_dict() for obj in obj_list]
                                 })
