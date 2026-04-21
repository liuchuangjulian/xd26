import logging
from js_kits.except_kits.except_kits import FastapiResult
from fastapi import Request
from wechatpayv3 import WeChatPay

logger = logging.getLogger(__name__)


class UnifiedPayCallback:
    """
    统一支付回调处理器
    根据商户订单号前缀识别订单类型并分发到对应的处理器
    """
    ORDER_TYPE_MEMBERSHIP = "MEM"  # 会员订单前缀
    ORDER_TYPE_SHOPPING = "SHOP"  # 购物订单前缀

    def __init__(self,
                 wx_pay: WeChatPay,
                 handle_membership_pay_callback=None,
                 handle_shopping_order_pay_callback=None):
        self.wx_pay = wx_pay
        self.handle_membership_pay_callback = handle_membership_pay_callback
        self.handle_shopping_order_pay_callback = handle_shopping_order_pay_callback

    async def execute(self, request: Request) -> None:
        """处理微信支付回调"""
        body = await request.body()
        result = self.wx_pay.callback(request.headers, body)

        if result and result.get('event_type') == 'TRANSACTION.SUCCESS':
            resp = result.get('resource')
            callback_data = {
                'out_trade_no': resp.get('out_trade_no'),
                'transaction_id': resp.get('transaction_id'),
                'amount': resp.get('amount')
            }

            out_trade_no = callback_data.get('out_trade_no')
            logger.info(f"收到支付回调 out_trade_no:{out_trade_no}")

            # 根据订单号前缀识别订单类型
            if out_trade_no.startswith(self.ORDER_TYPE_MEMBERSHIP):
                # 会员订单
                if self.handle_membership_pay_callback:
                    result = await self.handle_membership_pay_callback.execute(callback_data)
                    raise FastapiResult(result)
                else:
                    logger.error("会员支付回调处理器未配置")
                    raise FastapiResult({'code': 'FAIL', 'message': '处理器未配置'})
            elif out_trade_no.startswith(self.ORDER_TYPE_SHOPPING):
                # 购物订单
                if self.handle_shopping_order_pay_callback:
                    result = await self.handle_shopping_order_pay_callback.execute(callback_data)
                    raise FastapiResult(result)
                else:
                    logger.error("购物订单支付回调处理器未配置")
                    raise FastapiResult({'code': 'FAIL', 'message': '处理器未配置'})
            else:
                logger.error(f"未知订单类型: {out_trade_no}")
                raise FastapiResult({'code': 'FAIL', 'message': '未知订单类型'})
        else:
            logger.error(f"微信回调验证失败或事件类型不匹配: {result}")
            raise FastapiResult({'code': 'FAILED', 'message': '失败'})
