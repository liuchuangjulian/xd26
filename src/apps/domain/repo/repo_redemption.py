from js_kits.fastapi_kits.repo_base import BaseRepository
from sqlalchemy import text
from apps.domain.entities.redemption_history import RedemptionHistory


class RedemptionRepository(BaseRepository):

    async def ini(self, session):
        create_redemption_sql = """CREATE TABLE IF NOT EXISTS `redemption_history` (
              `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
              `uid` bigint unsigned DEFAULT NULL COMMENT '用户id',
              `card_number` varchar(100) NOT NULL COMMENT '卡号',
              `redeemed_at` datetime NOT NULL COMMENT '兑换时间',
              `deleted_at` datetime DEFAULT NULL COMMENT '删除时间',
              PRIMARY KEY (`id`),
              KEY `ix_redemption_history_uid` (`uid`),
              KEY `ix_redemption_history_card_number` (`card_number`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='兑换记录';
        """
        await session.execute(text(create_redemption_sql))

