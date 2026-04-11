import logging
from js_kits.except_kits.except_kits import FastapiResult

from apps.domain.entities.cart import CartEntity
from apps.domain.entities.products import ProductsEntity
from apps.domain.repo.repo_cart import CartRepository

logger = logging.getLogger(__name__)


class QueryCart:
    def __init__(self, repo: CartRepository):
        self.repo = repo

    async def query(self, uid, is_in_black) -> None:
        async with self.repo.session as session:
            _, obj_list = await self.repo.get_list(session, equal_maps={"uid": uid}, with_total=False)
            if obj_list:
                obj = obj_list[0]
            else:
                obj = CartEntity(uid=uid)
                await self.repo.add(session, obj)
            _, product_list = await self.repo.get_list(session, page_size=-1,
                                                       Entity=ProductsEntity, in_maps={"id":  obj.get_p_ids()},
                                                       with_total=False)
            raise FastapiResult({"msg": "ok",
                                 "data": obj.to_dict({p_obj.id: p_obj.to_dict(is_in_black) for p_obj in product_list})
                                 })
