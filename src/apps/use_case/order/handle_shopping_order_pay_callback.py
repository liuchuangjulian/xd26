import logging
from js_kits.except_kits.except_kits import FastapiResult
from apps.domain.entities.order import OrderStatus
from apps.domain.repo.repo_order import OrderRepository

logger = logging.getLogger(__name__)


class HandleShoppingOrderPayCallback:
    def __init__(self,
                 order_repo: OrderRepository):
        self.order_repo = order_repo

    async def execute(self, callback_data: dict) -> dict:
        """处理微信支付回调 - 购物订单"""
        out_trade_no = callback_data.get('out_trade_no')
        transaction_id = callback_data.get('transaction_id')
        total_amount = callback_data.get('amount', {}).get('total')

        logger.info(f"收到购物订单支付回调 out_trade_no:{out_trade_no}, transaction_id:{transaction_id}, amount:{total_amount}")

        async with self.order_repo.session as session:
            # 查询订单
            _, order_list = await self.order_repo.get_list(
                session,
                equal_maps={"out_trade_no": out_trade_no},
                with_total=False
            )

            if not order_list:
                logger.error(f"购物订单不存在: {out_trade_no}")
                return {'code': 'FAIL', 'message': '订单不存在'}

            order = order_list[0]

            # 检查订单状态
            if order.status == OrderStatus.Payed.value:
                logger.info(f"购物订单已支付: {out_trade_no}")
                return {'code': 'SUCCESS', 'message': '订单已处理'}

            if order.status != OrderStatus.Ordered.value:
                logger.error(f"购物订单状态异常: {out_trade_no}, status: {order.status}")
                return {'code': 'FAIL', 'message': '订单状态异常'}

            # 验证金额
            expected_amount = int((order.total - order.discount) * 100) if order.discount else int(order.total * 100)
            if expected_amount != total_amount:
                logger.error(f"金额不匹配: {out_trade_no}, expected:{expected_amount}, callback:{total_amount}")
                return {'code': 'FAIL', 'message': '金额不匹配'}

            # 更新订单状态为已支付
            order.mark_as_paid(transaction_id)
            await self.order_repo.add(session, order)

            logger.info(f"购物订单支付成功处理完成: {out_trade_no}")
            return {'code': 'SUCCESS', 'message': '成功'}
