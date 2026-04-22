import datetime
import logging
from js_kits.except_kits.except_kits import FastapiResult, ClientError
from apps.domain.entities.coupons import Coupon
from apps.domain.entities.order_line import OrderLineEntity
from apps.domain.entities.products import ProductsEntity
from apps.domain.repo.repo_order import OrderRepository

logger = logging.getLogger(__name__)


class UseCasePreCreateOrder:
    def __init__(self, repo: OrderRepository):
        self.repo = repo

    async def calc_best_coupon(self, session, uid, order_line_list):
        """计算最优优惠券"""
        best_coupon, max_discount = None, 0
        today = datetime.datetime.today()
        _, coupon_list = await self.repo.get_list(
            session,
            Entity=Coupon,
            in_maps={"uid": [uid, -1]},
            with_total=False,
            ge_maps={"effected_at": today},
            le_maps={"expired_at": today},
        )
        for coupon in coupon_list:
            discount = coupon.calc_discount(order_line_list)
            if discount > max_discount:
                max_discount = discount
                best_coupon = coupon
        return best_coupon, max_discount

    async def get_coupon_by_id(self, session, uid, coupon_id, order_line_list):
        """根据ID获取用户的优惠券"""
        _, coupon_list = await self.repo.get_list(
            session,
            Entity=Coupon,
            equal_maps={"uid": uid, "id": coupon_id},
            with_total=False
        )
        if not coupon_list:
            raise ClientError()
        coupon = coupon_list[0]
        return coupon, coupon.calc_discount(order_line_list)

    def calc_delivery_fee(self, order_line_list):
        """计算配送费"""
        return 600

    async def get_product_list(self, session, pids):
        # 查询商品信息
        pids = list(set(pids))
        _, product_list = await self.repo.get_list(
            session,
            Entity=ProductsEntity,
            in_maps={"id": pids},
            with_total=False
        )
        if not product_list or len(product_list) < len(pids):
            raise ClientError()
        return product_list

    async def execute(self, uid, p_id_count_list, coupon_id=0):
        p_id_map = {item["p_id"]: item["count"] for item in p_id_count_list}

        async with self.repo.session as session:
            product_list = await self.get_product_list(session, list(p_id_map))

            order_line_list = [OrderLineEntity(product, p_id_map[product.id]) for product in product_list]
            raw_total = sum([order_obj.amount for order_obj in order_line_list])
            if coupon_id > 0:
                best_coupon, discount = await self.get_coupon_by_id(session, uid, coupon_id, order_line_list)
            else:
                best_coupon, discount = await self.calc_best_coupon(session, uid, raw_total)
            # 计算配送费
            delivery_fee = self.calc_delivery_fee(raw_total)
            # 计算最终总价
            total = max(raw_total - discount + delivery_fee, 0)
            raise FastapiResult({
                "raw_total": str(round(raw_total / 100, 2)),
                "delivery_fee": str(round(delivery_fee / 100, 2)),
                "discount": str(round(discount / 100, 2)),
                "total": str(round(total / 100, 2)),
                "coupon": best_coupon.to_dict() if best_coupon else {}
            })
