import logging
import datetime
import os
from random import sample
from string import ascii_letters, digits
from datetime import datetime as dt
from wechatpayv3 import WeChatPayType
from js_kits.except_kits.except_kits import FastapiResult, ClientError
from apps.domain.entities.order import OrderEntity, OrderStatus
from apps.domain.repo.repo_order import OrderRepository
from apps.domain.repo.repo_user import UserRepository

logger = logging.getLogger(__name__)


class CreateShoppingOrderPay:
    def __init__(self,
                 order_repo: OrderRepository,
                 user_repo: UserRepository,
                 wx_pay: WeChatPayType):
        self.order_repo = order_repo
        self.user_repo = user_repo
        self.wx_pay = wx_pay

    async def get_order_obj(self, session, order_id, uid):
        # 获取订单信息
        _, order_list = await self.order_repo.get_list(
            session,
            equal_maps={"id": order_id, "uid": uid},
            with_total=False
        )
        if not order_list:
            raise ClientError({"msg": "订单不存在", "code": -1})
        order = order_list[0]
        return order

    async def get_user_obj(self, session, uid):
        # 获取用户对象
        _, user_list = await self.user_repo.get_list(
            session,
            equal_maps={"id": uid},
            with_total=False
        )
        if not user_list:
            raise ClientError({"msg": "用户不存在", "code": -1})
        user = user_list[0]
        if not user.wechat_openid:
            raise ClientError({"msg": "用户未绑定微信", "code": -1})
        return user

    async def execute(self, uid, order_id) -> None:
        async with self.order_repo.session as session:
            order_obj = await self.get_order_obj(session, order_id, uid)
            user = await self.get_user_obj(session, uid)

            # 检查订单状态，只有未支付订单才能发起支付
            if order_obj.status != OrderStatus.Ordered.value:
                raise ClientError({"msg": "订单状态异常，无法支付", "code": -1})

            # 如果订单已有商户订单号且在5分钟内，直接使用
            if order_obj.out_trade_no:
                time_diff = datetime.datetime.now() - order_obj.updated_at
                if time_diff.seconds < 300:  # 5分钟
                    return await self._create_wx_pay_params(order_obj, user)

            # 生成新的商户订单号
            order_obj.out_trade_no = OrderEntity.generate_out_trade_no()
            await self.order_repo.add(session, order_obj)
            await session.flush()
            return await self._create_wx_pay_params(order_obj, user)

    async def _create_wx_pay_params(self, order_obj, user):
        """创建微信支付参数"""
        try:
            # 计算实际支付金额（分）
            total_fee = int((order_obj.total - order_obj.discount) * 100) if order_obj.discount else int(order_obj.total * 100)

            # 调用微信支付统一下单
            code, message = self.wx_pay.pay(
                description=f"购物支付-{order_obj.main_info}",
                out_trade_no=str(order_obj.out_trade_no),
                amount={"total": total_fee},
                pay_type=WeChatPayType.JSAPI,
                payer={'openid': user.wechat_openid}
            )
            logger.info(f"微信预支付 code:{code}, message:{message}")
            if code not in range(200, 300):
                raise ClientError({"msg": f"微信支付下单失败: {message}", "code": -1})

            result = isinstance(message, str) and eval(message) or message
            prepay_id = result.get('prepay_id')

            # 生成小程序支付参数
            APPID = os.getenv("WX_APP_ID")
            now = dt.now()
            timestamp = str(int(dt.timestamp(now)))
            noncestr = ''.join(sample(ascii_letters + digits, 30))
            package = 'prepay_id=' + prepay_id
            paysign = self.wx_pay.sign([APPID, timestamp, noncestr, package])
            signtype = 'RSA'
            result_dict = {
                'appId': APPID,
                'timeStamp': timestamp,
                'nonceStr': noncestr,
                'package': 'prepay_id=%s' % prepay_id,
                'signType': signtype,
                'out_trade_no': order_obj.out_trade_no,
                'paySign': paysign
            }
            raise FastapiResult({
                "msg": "ok",
                "data": result_dict
            })
        except ClientError:
            raise
        except Exception as e:
            logger.error(f"创建微信支付参数失败: {str(e)}")
            raise ClientError({"msg": f"创建支付订单失败: {str(e)}", "code": -1})
