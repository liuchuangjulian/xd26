import logging
from except_kits.except_kits import FastapiResult
from apps.domain.entities.old.repo_community import CommunityRepository

logger = logging.getLogger(__name__)


class QueryCommunity:
    def __init__(self, repo: CommunityRepository):
        self.repo = repo

    async def query(self, page, page_size) -> None:
        async with self.repo.session as session:
            total, obj_list = await self.repo.get_list(session, page=page, page_size=page_size)
            raise FastapiResult({"msg": "ok",
                                 "total": total,
                                 "page": page,
                                 "page_size": page_size,
                                 "data": [obj.to_dict() for obj in obj_list]
                                 })
