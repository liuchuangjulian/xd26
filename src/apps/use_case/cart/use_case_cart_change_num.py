import logging
from js_kits.except_kits.except_kits import FastapiResult
from apps.domain.entities.cart import CartEntity
from apps.domain.entities.products import ProductsEntity
from apps.domain.repo.repo_cart import CartRepository
from sqlalchemy.orm.attributes import flag_modified

logger = logging.getLogger(__name__)


class UseCaseCartChangeNum:
    def __init__(self, repo: CartRepository):
        self.repo = repo

    async def execute(self, uid, p_id, num, dif) -> None:
        async with self.repo.session as session:
            _, product_list = await self.repo.get_list(session, Entity=ProductsEntity, equal_maps={"id": p_id},
                                                       with_total=False)
            if not product_list:
                raise Exception()
            product_obj = product_list[0]
            _, obj_list = await self.repo.get_list(session, equal_maps={"uid": uid}, with_total=False)
            if obj_list:
                obj = obj_list[0]
            else:
                obj = CartEntity().init_and_add_one(uid, p_id)

            obj.set_count(p_id, num, product_obj.get_limit_count(), dif)
            flag_modified(obj, "p_id_info_map")
            flag_modified(obj, "p_list")
            await self.repo.add(session, obj)
            raise FastapiResult({"msg": "ok"})
