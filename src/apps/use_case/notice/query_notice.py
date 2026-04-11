import logging
from js_kits.except_kits.except_kits import FastapiResult
from apps.domain.repo.repo_config import ConfigRepository

logger = logging.getLogger(__name__)


class QueryNotice:
    def __init__(self, repo: ConfigRepository):
        self.repo = repo

    async def query(self) -> None:
        async with self.repo.session as session:
            _, obj_list = await self.repo.get_list(session,
                                                   equal_maps={"key": "notice", "is_active": 1}, with_total=False)
            print(obj_list)
            if obj_list:
                raise FastapiResult({"data": obj_list[0].extend_property})
            else:
                raise FastapiResult({"data": {"show": 0, "title": "", "content": ""}})
