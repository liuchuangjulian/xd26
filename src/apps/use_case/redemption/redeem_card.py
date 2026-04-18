import logging
from decimal import Decimal
from datetime import datetime
from js_kits.except_kits.except_kits import FastapiResult, ClientError
from apps.domain.repo.repo_user import UserRepository
from apps.domain.repo.repo_redemption import RedemptionRepository
from apps.domain.entities.redemption_card import RedemptionCard
from apps.domain.entities.redemption_history import RedemptionHistory

logger = logging.getLogger(__name__)


class RedeemCardUseCase:
    def __init__(self, user_repo: UserRepository, redemption_repo: RedemptionRepository):
        self.user_repo = user_repo
        self.redemption_repo = redemption_repo

    async def execute(self, uid, card_number):
        """执行兑换操作"""
        try:
            async with self.user_repo.session as session:
                logger.info(f"开始兑换：uid={uid}, card_number={card_number}")

                # 1. 查询兑换卡
                card = await self.redemption_repo.get_card_by_number(session, card_number)

                if not card:
                    raise ClientError({"msg": "兑换卡不存在"})

                logger.info(f"兑换卡信息：{card.to_dict()}")

                # 2. 检查卡状态
                is_valid, error_msg = card.is_valid()
                if not is_valid:
                    raise ClientError({"msg": error_msg})

                # 3. 获取用户当前余额
                _, user_list = await self.user_repo.get_list(
                    session,
                    equal_maps={"id": uid},
                    with_total=False
                )

                if not user_list:
                    raise ClientError({"msg": "用户不存在"})

                user = user_list[0]
                current_balance = Decimal(str(user.balance)) if user.balance else Decimal('0.00')
                logger.info(f"用户当前余额：{current_balance}")

                # 4. 更新用户余额
                new_balance = current_balance + Decimal(str(card.amount))
                user.balance = new_balance
                await self.user_repo.add(session, user)

                # 5. 标记兑换卡为已使用
                await self.redemption_repo.mark_card_as_used(session, card, uid)

                # 6. 创建兑换记录
                history = RedemptionHistory(
                    uid=uid,
                    card_number=card_number,
                    amount=card.amount,
                    status=1,
                    redemption_time=datetime.now()
                )
                await self.redemption_repo.add(session, history)

                logger.info(f"兑换成功：uid={uid}, amount={card.amount}, new_balance={new_balance}")

                raise FastapiResult({
                    "msg": "兑换成功",
                    "data": {
                        "card_number": card_number,
                        "amount": float(card.amount),
                        "balance_before": float(current_balance),
                        "balance_after": float(new_balance)
                    }
                })
        except Exception as e:
            logger.error(f"兑换失败：{e}", exc_info=True)
            raise
