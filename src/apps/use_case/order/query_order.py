import logging
from js_kits.except_kits.except_kits import FastapiResult
from apps.domain.repo.repo_order import OrderRepository

logger = logging.getLogger(__name__)


class QueryOrder:
    def __init__(self, repo: OrderRepository):
        self.repo = repo

    async def query(self, uid, status, page, page_size) -> None:
        equal_maps = {"uid": uid}

        if status:
            equal_maps["status"] = status
        async with self.repo.session as session:
            total, order_list = await self.repo.get_list(session, page=page, page_size=page_size,
                                                       equal_maps=equal_maps,
                                                       )
            raise FastapiResult({"msg": "ok",
                                 "total": total,
                                 "page": page,
                                 "page_size": page_size,
                                 "data": [order_obj.to_dict() for order_obj in order_list]
                                 })
