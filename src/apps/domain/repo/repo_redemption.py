from js_kits.fastapi_kits.repo_base import BaseRepository
from sqlalchemy import text, select
from typing import Optional
import warnings
from apps.domain.entities.redemption_card import RedemptionCard


class RedemptionRepository(BaseRepository):

    async def ini(self, session):
        # 创建兑换卡表
        create_cards_sql = """CREATE TABLE IF NOT EXISTS `redemption_cards` (
              `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
              `card_number` varchar(100) NOT NULL COMMENT '卡号',
              `amount` decimal(10,2) NOT NULL DEFAULT '0.00' COMMENT '金额',
              `status` tinyint NOT NULL DEFAULT '0' COMMENT '状态:0-未使用,1-已使用,2-已失效',
              `expired_at` datetime DEFAULT NULL COMMENT '过期时间',
              `used_at` datetime DEFAULT NULL COMMENT '使用时间',
              `used_by` bigint unsigned DEFAULT NULL COMMENT '使用用户ID',
              `deleted_at` datetime DEFAULT NULL COMMENT '删除时间',
              `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
              `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
              PRIMARY KEY (`id`),
              UNIQUE KEY `uk_redemption_cards_card_number` (`card_number`),
              KEY `ix_redemption_cards_status` (`status`),
              KEY `ix_redemption_cards_used_by` (`used_by`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='兑换卡';
        """

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            await session.execute(text(create_cards_sql), execution_options={"warning": False})

    async def get_card_by_number(self, session, card_number: str) -> Optional[RedemptionCard]:
        """根据卡号查询兑换卡"""
        stmt = select(RedemptionCard).where(
            RedemptionCard.card_number == card_number,
            RedemptionCard.deleted_at == None
        )
        result = await session.execute(stmt)
        return result.scalars().first()

