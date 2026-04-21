import logging
from js_kits.except_kits.except_kits import FastapiResult
from wechatpayv3 import WeChatPay
from sqlalchemy.orm.attributes import flag_modified
from apps.domain.repo.repo_membership_order import MembershipOrderRepository
from apps.domain.repo.repo_order import OrderRepository

logger = logging.getLogger(__name__)


class UnifiedPayCallback:
    """
    统一支付回调处理器
    根据商户订单号前缀识别订单类型并分发到对应的处理器
    """

    # 订单类型前缀定义
    ORDER_TYPE_MEMBERSHIP = "MEM"
    ORDER_TYPE_SHOPPING = "SHOP"
    # 成功响应
    SUCCESS_RESPONSE = {'code': 'SUCCESS', 'message': '成功'}
    FAIL_RESPONSE = {'code': 'FAIL', 'message': '处理失败'}

    def __init__(self, wx_pay: WeChatPay, membership_order_repo: MembershipOrderRepository, order_repo: OrderRepository):
        self.wx_pay = wx_pay
        self.membership_order_repo = membership_order_repo
        self.order_repo = order_repo

    async def handle_membership_order(self, out_trade_no, resource):
        async with self.membership_order_repo.session as session:
            _, mo_list = await self.membership_order_repo.get_list(session, equal_maps={"out_trade_no": out_trade_no}, with_total=False)
            if not mo_list:
                raise FastapiResult(result={**self.FAIL_RESPONSE})
            mo_obj = mo_list[0]
            mo_obj.paid_from_wx(resource)
            flag_modified(mo_obj, "extend_property")
            await self.membership_order_repo.add(session, mo_obj)

    async def handle_order(self, out_trade_no, resource):
        async with self.order_repo.session as session:
            _, bo_list = await self.order_repo.get_list(session, equal_maps={"out_trade_no": out_trade_no}, with_total=False)
            if not bo_list:
                raise FastapiResult(result={**self.FAIL_RESPONSE})
            bo_obj = bo_list[0]
            bo_obj.paid_from_wx(resource)
            flag_modified(bo_obj, "extend_property")
            await self.order_repo.add(session, mo_obj)


    async def execute(self, headers, body) -> None:
        """处理微信支付回调"""
        out_trade_no, resource = await self._parse_wx_callback(headers, body)

        if out_trade_no.startswith(self.ORDER_TYPE_MEMBERSHIP):
            await self.handle_membership_order(out_trade_no, resource)
        elif out_trade_no.startswith(self.ORDER_TYPE_MEMBERSHIP):
            ...

        raise FastapiResult(result={**self.SUCCESS_RESPONSE})

    async def _parse_wx_callback(self, headers, body):
        """解析微信支付回调"""
        result = self.wx_pay.callback(headers, body)
        if not result or result.get('event_type') != 'TRANSACTION.SUCCESS':
            logger.error(f"微信回调验证失败或事件类型不匹配: {result}")
            raise FastapiResult({'code': 'FAILED', 'message': '回调验证失败'})
        logger.info(f"收到支付回调 resource:{result.get('resource')}")
        return result.get('resource').get('out_trade_no'), result.get('resource')


