import logging
from js_kits.except_kits.except_kits import FastapiResult
from apps.domain.repo.repo_order_line import OrderLineRepository

logger = logging.getLogger(__name__)


class QueryOrderLine:
    def __init__(self, repo: OrderLineRepository):
        self.repo = repo

    async def query(self, uid, order_id, page, page_size) -> None:
        equal_maps = {"uid": uid, "order_id": order_id}

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
