import logging
from js_kits.except_kits.except_kits import FastapiResult

logger = logging.getLogger(__name__)


class UnifiedPayCallback:
    """
    统一支付回调处理器
    根据商户订单号前缀识别订单类型并分发到对应的处理器
    """
    ORDER_TYPE_MEMBERSHIP = "MEM"  # 会员订单前缀
    ORDER_TYPE_SHOPPING = "SHOP"  # 购物订单前缀

    def __init__(self,
                 handle_membership_pay_callback=None,
                 handle_shopping_order_pay_callback=None):
        self.handle_membership_pay_callback = handle_membership_pay_callback
        self.handle_shopping_order_pay_callback = handle_shopping_order_pay_callback

    async def execute(self, callback_data: dict) -> dict:
        """处理微信支付回调"""
        out_trade_no = callback_data.get('out_trade_no')

        logger.info(f"收到支付回调 out_trade_no:{out_trade_no}")

        # 根据订单号前缀识别订单类型
        if out_trade_no.startswith(self.ORDER_TYPE_MEMBERSHIP):
            # 会员订单
            if self.handle_membership_pay_callback:
                return await self.handle_membership_pay_callback.execute(callback_data)
            else:
                logger.error("会员支付回调处理器未配置")
                return {'code': 'FAIL', 'message': '处理器未配置'}
        elif out_trade_no.startswith(self.ORDER_TYPE_SHOPPING):
            # 购物订单
            if self.handle_shopping_order_pay_callback:
                return await self.handle_shopping_order_pay_callback.execute(callback_data)
            else:
                logger.error("购物订单支付回调处理器未配置")
                return {'code': 'FAIL', 'message': '处理器未配置'}
        else:
            logger.error(f"未知订单类型: {out_trade_no}")
            return {'code': 'FAIL', 'message': '未知订单类型'}
