import logging
from js_kits.except_kits.except_kits import FastapiResult
from apps.domain.entities.coupons import Coupon
from apps.domain.entities.products import ProductsEntity
from apps.domain.repo.repo_order import OrderRepository

logger = logging.getLogger(__name__)


class UseCasePreCreateOrder:
    def __init__(self, repo: OrderRepository):
        self.repo = repo

    async def calc_best_coupon(self, session, uid, total):
        """计算最优优惠券"""
        best_coupon = None
        max_discount = 0

        _, coupon_list = await self.repo.get_list(
            session,
            Entity=Coupon,
            equal_maps={"uid": uid},
            with_total=False
        )

        for coupon in coupon_list:
            discount = coupon.calc_discount(total)
            if discount > max_discount:
                max_discount = discount
                best_coupon = coupon

        return best_coupon, max_discount

    async def get_coupon_by_id(self, session, uid, coupon_id):
        """根据ID获取用户的优惠券"""
        if coupon_id == 0:
            return None, 0

        _, coupon_list = await self.repo.get_list(
            session,
            Entity=Coupon,
            equal_maps={"uid": uid, "id": coupon_id},
            with_total=False
        )

        if coupon_list:
            coupon = coupon_list[0]
            return coupon, 0
        else:
            return None, 0

    def calc_delivery_fee(self, total):
        """计算配送费（可以根据订单金额或距离计算）"""
        # 简单的配送费计算规则：
        # 订单金额满99元免配送费，否则6元
        if total >= 9900:  # 99.00元
            return 0
        else:
            return 600  # 6.00元

    async def execute(self, uid, p_id_count_list, coupon_id=0) -> None:
        p_id_map = {item["p_id"]: item["count"] for item in p_id_count_list}
        print(f"DEBUG: 预创建订单: uid={uid}, p_id_map={p_id_map}, coupon_id={coupon_id}")

        async with self.repo.session as session:
            # 查询商品信息
            _, product_list = await self.repo.get_list(
                session,
                Entity=ProductsEntity,
                in_maps={"id": list(p_id_map)},
                with_total=False
            )

            print(f"DEBUG: 查询到商品: {len(product_list)}个")

            if not product_list:
                print("DEBUG: 商品不存在")
                return {
                    "products": [],
                    "raw_total": "0.00",
                    "delivery_fee": "0.00",
                    "discount": "0.00",
                    "total": "0.00",
                    "coupon": None
                }

            # 构建商品列表，计算小计
            products_detail = []
            raw_total = 0

            for product in product_list:
                count = p_id_map[product.id]
                subtotal = product.price * count
                raw_total += subtotal

                products_detail.append({
                    "p_id": product.id,
                    "name": product.name,
                    "img": product.img,
                    "price": str(round(product.price / 100, 2)),
                    "count": count,
                    "subtotal": str(round(subtotal / 100, 2))
                })

            print(f"DEBUG: 商品详情: {products_detail}, 总价: {raw_total}")

            # 计算优惠券
            if coupon_id > 0:
                # 使用指定的优惠券
                best_coupon, _ = await self.get_coupon_by_id(session, uid, coupon_id)
                if best_coupon:
                    discount = best_coupon.calc_discount(raw_total)
                    print(f"DEBUG: 使用指定优惠券: {best_coupon}, 优惠: {discount}")
                else:
                    # 指定的优惠券不存在，使用最优优惠券
                    best_coupon, discount = await self.calc_best_coupon(session, uid, raw_total)
                    print(f"DEBUG: 指定优惠券不存在，使用最优优惠券: {best_coupon}, 优惠: {discount}")
            else:
                # 自动计算最优优惠券
                best_coupon, discount = await self.calc_best_coupon(session, uid, raw_total)
                print(f"DEBUG: 自动选择最优优惠券: {best_coupon}, 优惠: {discount}")

            # 计算配送费
            delivery_fee = self.calc_delivery_fee(raw_total)

            # 计算最终总价
            total = max(raw_total - discount + delivery_fee, 0)

            # 构建优惠券信息
            coupon_info = None
            if best_coupon:
                coupon_info = {
                    "id": best_coupon.id,
                    "title": best_coupon.title,
                    "discount": str(round(discount / 100, 2))
                }

            result_data = {
                "products": products_detail,
                "raw_total": str(round(raw_total / 100, 2)),
                "delivery_fee": str(round(delivery_fee / 100, 2)),
                "discount": str(round(discount / 100, 2)),
                "total": str(round(total / 100, 2)),
                "coupon": coupon_info
            }

            print(f"DEBUG: 完整返回数据: {result_data}")
            print(f"DEBUG: 商品数量: {len(products_detail)}")

            return result_data

