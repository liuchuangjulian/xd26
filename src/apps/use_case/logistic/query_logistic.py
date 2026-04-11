import logging
from js_kits.except_kits.except_kits import FastapiResult
from apps.domain.repo.repo_logistic import LogisticRepository

logger = logging.getLogger(__name__)


class QueryLogistic:
    def __init__(self, repo: LogisticRepository):
        self.repo = repo

    async def query(self, uid, order_id) -> None:
        async with self.repo.session as session:
            # "uid": uid,
            _, obj_list = await self.repo.get_list(session, equal_maps={"order_id": order_id},
                                                   with_total=False, with_none_deleted=False)
            raise FastapiResult({"msg": "ok",
                                 "data": [obj.to_dict() for obj in obj_list]
                                 })
