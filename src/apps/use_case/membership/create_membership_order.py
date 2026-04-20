import logging
import datetime
import os
from random import sample
from string import ascii_letters, digits
from datetime import datetime as dt
from wechatpayv3 import WeChatPayType
from js_kits.except_kits.except_kits import FastapiResult, ClientError
from apps.domain.entities.membership_order import MembershipOrderEntity, MembershipOrderStatus
from apps.domain.entities.user_membership import UserMembershipEntity
from apps.domain.repo.repo_membership_order import MembershipOrderRepository
from apps.domain.repo.repo_user_membership import UserMembershipRepository
from apps.domain.repo.repo_membership import MembershipRepository
from apps.domain.repo.repo_user import UserRepository

logger = logging.getLogger(__name__)


class CreateMembershipOrder:
    def __init__(self,
                 membership_order_repo: MembershipOrderRepository,
                 user_membership_repo: UserMembershipRepository,
                 membership_repo: MembershipRepository,
                 user_repo: UserRepository,
                 wx_pay: WeChatPayType):
        self.membership_order_repo = membership_order_repo
        self.user_membership_repo = user_membership_repo
        self.membership_repo = membership_repo
        self.user_repo = user_repo
        self.wx_pay = wx_pay

    async def execute(self, uid, membership_id) -> None:
        async with self.membership_order_repo.session as session:
            # 获取会员信息
            _, membership_list = await self.membership_repo.get_list(
                session,
                with_total=False,
                equal_maps={"id": membership_id}
            )
            if not membership_list:
                raise ClientError({"msg": "会员类型不存在", "code": -1})
            membership = membership_list[0]

            # 检查会员是否启用
            if membership.status != 1:
                raise ClientError({"msg": "该会员类型暂不可购买", "code": -1})

            # 获取用户信息
            _, user_list = await self.user_repo.get_list(
                session,
                equal_maps={"id": uid},
                with_total=False
            )
            if not user_list:
                raise ClientError({"msg": "用户不存在", "code": -1})
            user = user_list[0]

            # 检查是否有未支付的订单
            _, unpaid_orders = await self.membership_order_repo.get_list(
                session,
                equal_maps={"uid": uid, "membership_id": membership_id, "status": MembershipOrderStatus.UnPaid.value},
                with_total=False
            )
            if unpaid_orders:
                # 如果有未支付订单，检查是否在有效期内（5分钟）
                latest_order = unpaid_orders[0]
                time_diff = datetime.datetime.now() - latest_order.created_at
                if time_diff.seconds < 300:  # 5分钟
                    # 继续使用原订单
                    return await self._create_wx_pay_params(latest_order, user, membership)
                else:
                    # 取消旧订单
                    latest_order.status = MembershipOrderStatus.Cancelled.value
                    await self.membership_order_repo.add(session, latest_order)

            # 创建新订单
            total_fee = int(membership.price * 100)  # 转换为分
            out_trade_no = self._generate_out_trade_no()

            order = MembershipOrderEntity(
                uid=uid,
                membership_id=membership_id,
                out_trade_no=out_trade_no,
                transaction_id="",
                total_fee=total_fee,
                status=MembershipOrderStatus.UnPaid.value,
                membership_info={
                    "id": membership.id,
                    "name": membership.name,
                    "price": float(membership.price),
                    "duration": membership.duration,
                    "description": membership.description,
                },
                pay_time=None,
                extend_property={}
            )
            await self.membership_order_repo.add(session, order)
            await session.flush()  # 确保订单已保存

            return await self._create_wx_pay_params(order, user, membership)

    async def _create_wx_pay_params(self, order, user, membership):
        """创建微信支付参数"""
        try:
            # 获取用户的openid
            user_dict = user.to_dict()
            openid = user_dict.get("openid")
            if not openid:
                raise ClientError({"msg": "用户未绑定微信", "code": -1})

            # 调用微信支付统一下单
            payer = {'openid': openid}
            code, message = self.wx_pay.pay(
                description=f"购买会员-{membership.name}",
                out_trade_no=str(order.out_trade_no),
                amount={"total": order.total_fee},
                pay_type=WeChatPayType.JSAPI,
                payer=payer
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
                'out_trade_no': order.out_trade_no,
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

    def _generate_out_trade_no(self):
        """生成商户订单号"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        random_str = ''.join(sample(digits, 6))
        return f"MEM{timestamp}{random_str}"
