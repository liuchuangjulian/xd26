import logging
from js_kits.except_kits.except_kits import FastapiResult
from apps.domain.entities.membership_order import MembershipOrderStatus
from apps.domain.repo.repo_membership_order import MembershipOrderRepository
from apps.domain.repo.repo_user_membership import UserMembershipRepository
from apps.domain.entities.user_membership import UserMembershipEntity

logger = logging.getLogger(__name__)


class HandleMembershipPayCallback:
    def __init__(self,
                 membership_order_repo: MembershipOrderRepository,
                 user_membership_repo: UserMembershipRepository):
        self.membership_order_repo = membership_order_repo
        self.user_membership_repo = user_membership_repo

    async def execute(self, callback_data: dict) -> dict:
        """处理微信支付回调"""
        out_trade_no = callback_data.get('out_trade_no')
        transaction_id = callback_data.get('transaction_id')
        total_amount = callback_data.get('amount', {}).get('total')

        logger.info(f"收到会员支付回调 out_trade_no:{out_trade_no}, transaction_id:{transaction_id}, amount:{total_amount}")

        async with self.membership_order_repo.session as session:
            # 查询订单
            _, order_list = await self.membership_order_repo.get_list(
                session,
                equal_maps={"out_trade_no": out_trade_no},
                with_total=False
            )

            if not order_list:
                logger.error(f"订单不存在: {out_trade_no}")
                return {'code': 'FAIL', 'message': '订单不存在'}

            order = order_list[0]

            # 检查订单状态
            if order.status == MembershipOrderStatus.Paid.value:
                logger.info(f"订单已支付: {out_trade_no}")
                return {'code': 'SUCCESS', 'message': '订单已处理'}

            if order.status != MembershipOrderStatus.UnPaid.value:
                logger.error(f"订单状态异常: {out_trade_no}, status: {order.status}")
                return {'code': 'FAIL', 'message': '订单状态异常'}

            # 验证金额
            if order.total_fee != total_amount:
                logger.error(f"金额不匹配: {out_trade_no}, order:{order.total_fee}, callback:{total_amount}")
                return {'code': 'FAIL', 'message': '金额不匹配'}

            # 更新订单状态
            order.mark_as_paid(transaction_id)
            await self.membership_order_repo.add(session, order)

            # 创建用户会员记录
            await self._create_user_membership(session, order)

            logger.info(f"会员支付成功处理完成: {out_trade_no}")
            return {'code': 'SUCCESS', 'message': '成功'}

    async def _create_user_membership(self, session, order):
        """创建用户会员记录"""
        import datetime

        # 查询用户已有会员记录
        _, existing_memberships = await self.user_membership_repo.get_list(
            session,
            equal_maps={"uid": order.uid},
            with_total=False
        )

        # 计算开始和结束日期
        start_day = datetime.date.today()
        duration = order.membership_info.get("duration", 0)
        end_day = start_day + datetime.timedelta(days=duration)

        # 如果有有效会员，从原结束日期开始计算
        if existing_memberships:
            latest_membership = max(existing_memberships, key=lambda x: x.end_day)
            if latest_membership.end_day >= start_day:
                start_day = latest_membership.end_day
                end_day = start_day + datetime.timedelta(days=duration)

        # 创建用户会员记录
        obj = UserMembershipEntity(
            uid=order.uid,
            membership_id=order.membership_id,
            membership_info=order.membership_info,
            start_day=start_day,
            end_day=end_day,
            extend_property={"order_id": order.id}
        )
        await self.user_membership_repo.add(session, obj)

        logger.info(f"创建用户会员记录成功 uid:{order.uid}, membership_id:{order.membership_id}, end_day:{end_day}")
