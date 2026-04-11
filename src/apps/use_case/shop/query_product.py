import logging
from js_kits.except_kits.except_kits import FastapiResult
from apps.domain.repo.repo_products import ProductRepository

logger = logging.getLogger(__name__)


class QueryProducts:
    def __init__(self, repo: ProductRepository):
        self.repo = repo

    async def query(self, category_id=None, name=None, page_size=10, page=1) -> None:
        if page_size > 10:
            page_size = 10
        key_contains_list, like_maps = None, {}
        if category_id:
            key_contains_list = ["category_id_list", category_id]
        if name:
            like_maps["name"] = name
        async with self.repo.session as session:
            total, obj_list = await self.repo.get_list(session, like_maps=like_maps,
                                                       page=page, page_size=page_size,
                                                       key_contains_list=key_contains_list)
            raise FastapiResult({"msg": "ok",
                                 "data": {
                                     "total": total,
                                     "page": page,
                                     "page_size": page_size,
                                     "list": [obj.to_dict() for obj in obj_list]
                                 }
                                 })
