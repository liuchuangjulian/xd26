from fastapi import Request
from fastapi import APIRouter
from fastapi_injector import Injected
import logging

from apps.use_case.pay.unified_pay_callback import UnifiedPayCallback

router_pay = APIRouter(prefix="/pay", tags=["支付"])
logger = logging.getLogger(__name__)


@router_pay.post("/notify", summary="统一支付回调")
async def unified_pay_notify(request: Request,
                             use_case: UnifiedPayCallback = Injected(UnifiedPayCallback)):
    """微信支付回调通知 - 兼容会员订单和购物订单"""
    await use_case.execute(request.headers, await request.body())
'''
# 微信支付回调通知（由微信服务器调用，无需手动测试）
# curl -X 'POST' \
#   'http://localhost:8080/api/pay/notify' \
#   -H 'Content-Type: application/json' \
#   -H 'Wechatpay-Signature: xxx' \
#   -H 'Wechatpay-Timestamp: xxx' \
#   -H 'Wechatpay-Nonce: xxx' \
#   -H 'Wechatpay-Serial: xxx' \
#   -d '{"event_type": "TRANSACTION.SUCCESS", "resource": {"ciphertext": "xxx"}}'
'''
