import logging
from js_kits.except_kits.except_kits import FastapiResult
from apps.domain.repo.repo_membership import MembershipRepository

logger = logging.getLogger(__name__)


class QueryMembership:
    def __init__(self, repo: MembershipRepository):
        self.repo = repo

    async def query(self, uid) -> None:
        async with self.repo.session as session:
            total, obj_list = await self.repo.get_list(
                session,
                # equal_maps={"status": 1},
                order_by_list=["show_index"]
            )
            raise FastapiResult({
                "msg": "ok",
                "data": [obj.to_dict() for obj in obj_list]
            })
