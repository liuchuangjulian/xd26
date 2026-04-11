import logging
import datetime
from decimal import Decimal
from js_kits.except_kits.except_kits import FastapiResult, ClientError
from apps.domain.repo.repo_user import UserRepository
from sqlalchemy import select, text

logger = logging.getLogger(__name__)


class RedeemCardUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def execute(self, uid, card_number):
        """执行兑换操作"""
        try:
            async with self.user_repo.session as session:
                logger.info(f"开始兑换：uid={uid}, card_number={card_number}")

                # 查询兑换卡
                result = await session.execute(
                    text("SELECT * FROM redemption_cards WHERE card_number = :card_number AND deleted_at IS NULL"),
                    {"card_number": card_number}
                )
                card = result.fetchone()

                if not card:
                    raise ClientError({"msg": "兑换卡不存在"})

                card_dict = dict(card._mapping)
                logger.info(f"兑换卡信息：{card_dict}")

                # 检查卡状态
                if card_dict['status'] == 1:
                    raise ClientError({"msg": "该兑换卡已使用"})
                elif card_dict['status'] == 2:
                    raise ClientError({"msg": "该兑换卡已过期"})

                # 检查过期时间
                if card_dict['expired_at']:
                    expired_at = card_dict['expired_at']
                    if expired_at < datetime.datetime.now():
                        raise ClientError({"msg": "该兑换卡已过期"})

                # 获取用户当前余额
                result = await session.execute(
                    text("SELECT balance FROM user WHERE id = :uid"),
                    {"uid": uid}
                )
                user_balance = result.fetchone()

                if not user_balance:
                    raise ClientError({"msg": "用户不存在"})

                current_balance = Decimal(str(user_balance[0]))
                logger.info(f"用户当前余额：{current_balance}")

                # 更新用户余额
                new_balance = current_balance + Decimal(str(card_dict['amount']))
                await session.execute(
                    text("UPDATE user SET balance = :balance WHERE id = :uid"),
                    {"balance": new_balance, "uid": uid}
                )

                # 更新兑换卡状态
                await session.execute(
                    text("""
                        UPDATE redemption_cards
                        SET status = 1, used_at = NOW(), used_by = :uid
                        WHERE card_number = :card_number
                    """),
                    {"uid": uid, "card_number": card_number}
                )

                # 创建兑换记录
                await session.execute(
                    text("""
                        INSERT INTO redemption_history
                        (uid, card_number, amount, status, redemption_time)
                        VALUES (:uid, :card_number, :amount, 1, NOW())
                    """),
                    {
                        "uid": uid,
                        "card_number": card_number,
                        "amount": card_dict['amount']
                    }
                )

                logger.info(f"兑换成功：uid={uid}, amount={card_dict['amount']}, new_balance={new_balance}")

                raise FastapiResult({
                    "msg": "兑换成功",
                    "data": {
                        "card_number": card_number,
                        "amount": float(card_dict['amount']),
                        "balance_before": float(current_balance),
                        "balance_after": float(new_balance)
                    }
                })
        except Exception as e:
            logger.error(f"兑换失败：{e}", exc_info=True)
            raise
