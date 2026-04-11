import logging
from js_kits.except_kits.except_kits import FastapiResult
from apps.domain.repo.repo_address import AddressRepository

logger = logging.getLogger(__name__)


class QueryAddress:
    def __init__(self, repo: AddressRepository):
        self.repo = repo

    async def query(self, uid, selected, page, page_size) -> None:
        async with self.repo.session as session:
            equal_maps = {"uid": uid}
            if selected:
                equal_maps["selected"] = selected
            total, obj_list = await self.repo.get_list(session, equal_maps=equal_maps,
                                                       page=page, page_size=page_size)
            if total == 0 and selected:
                equal_maps.pop("selected", None)
                total, obj_list = await self.repo.get_list(session, equal_maps=equal_maps,
                                                           order_by_list=["-updated_at"],
                                                           page=1, page_size=1)
            raise FastapiResult({"msg": "ok",
                                 "total": total,
                                 "page": page,
                                 "page_size": page_size,
                                 "data": [obj.to_dict() for obj in obj_list]
                                 })
