import logging
from js_kits.except_kits.except_kits import FastapiResult
from apps.domain.repo.repo_category import CategoryRepository

logger = logging.getLogger(__name__)


class QueryCategory:
    def __init__(self, repo: CategoryRepository,
                 ):
        self.repo = repo

    async def query(self) -> None:
        async with self.repo.session as session:
            total, obj_list = await self.repo.get_list(session, order_by_list=["show_index"])
            raise FastapiResult({"msg": "ok",
                                 "data": [obj.to_dict() for obj in obj_list]
                                 })
