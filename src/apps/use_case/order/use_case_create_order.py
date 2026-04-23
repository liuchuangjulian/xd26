import logging
from js_kits.except_kits.except_kits import FastapiResult, ClientError
from apps.domain.entities.address import Address
from apps.domain.entities.coupons import Coupon
from apps.domain.entities.order import OrderEntity
from apps.domain.entities.order_line import OrderLineEntity
from apps.domain.entities.products import ProductsEntity
from apps.domain.repo.repo_order import OrderRepository

logger = logging.getLogger(__name__)


class UseCaseCreateOrder:
    def __init__(self, repo: OrderRepository):
        self.repo = repo

    async def get_address(self, session, address_id, uid):
        _, address_list = await self.repo.get_list(session, Entity=Address,
                                                   equal_maps={"id": address_id, "uid": uid},
                                                   with_total=False)
        if not address_list:
            raise ClientError({"msg": "地址不存在"})
        return address_list[0]

    async def get_coupon(self, session, coupon_id, uid):
        _, coupon_list = await self.repo.get_list(session, Entity=Coupon,
                                                  equal_maps={"id": coupon_id},
                                                  with_total=False)
        if not coupon_list or not coupon_list[0].can_user_use(uid):
            raise ClientError({"msg": "优惠券不存在或不可用"})
        return coupon_list[0]

    async def execute(self, uid, p_id_count_list, address_id, coupon_id) -> None:
        p_id_map = {item["p_id"]: item["count"] for item in p_id_count_list}
        async with self.repo.session as session:
            address_obj = await self.get_address(session, address_id, uid)
            coupon_obj = await self.get_coupon(session, coupon_id, uid) if coupon_id else None

            _, product_list = await self.repo.get_list(session, Entity=ProductsEntity, in_maps={"id": list(p_id_map)},
                                                       with_total=False)
            if not product_list or len(p_id_map) != len(product_list):
                raise ClientError({"msg": "产品异常"})
            order_obj = OrderEntity(uid=uid)
            await self.repo.add(session, order_obj)
            ol_list = [OrderLineEntity.build_from_product_with_order_id(p_obj, p_id_map[p_obj.id], order_obj.id, this_index) for this_index, p_obj in enumerate(product_list)]

            await self.repo.add_all(session, ol_list)
            order_obj.refresh_data_from_ol(ol_list)
            order_obj.set_address_obj(address_obj)
            if order_obj.set_coupon_obj(coupon_obj):
                discount = coupon_obj.calc_discount()
                order_obj.discount = discount
            await self.repo.add(session, order_obj)
            await self.repo.add(session, coupon_obj)
            raise FastapiResult({"msg": "ok",
                                 "data": order_obj.id
                                 })
