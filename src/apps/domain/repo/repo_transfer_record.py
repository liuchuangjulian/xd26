from js_kits.fastapi_kits.repo_base import BaseRepository
import warnings
from sqlalchemy import text


class TransferRecordRepository(BaseRepository):
    async def ini(self, session):
        create_biz_sql = """
                CREATE TABLE IF NOT EXISTS `transfer_record` (
                  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
                  `type` varchar(64) NOT NULL COMMENT '记录类型',
                  `uid` int NOT NULL COMMENT '用户id',
                  `amount` int NOT NULL COMMENT '交易金额（分）',
                  `amount_real` int NOT NULL COMMENT '实际金额（分）',
                  `amount_gift` int NOT NULL DEFAULT 0 COMMENT '赠送金额（分）',
                  `amount_coin_count` int NOT NULL DEFAULT 0 COMMENT '积分',
                  `op_uid` int DEFAULT NULL COMMENT '操作用户id',
                  `status` varchar(32) NOT NULL COMMENT '状态',
                  `extra` json DEFAULT NULL COMMENT '附加属性',
                  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                  `deleted_at` datetime DEFAULT NULL COMMENT '删除时间',
                  PRIMARY KEY (`id`),
                  KEY `ix_transfer_record_uid` (`uid`),
                  KEY `ix_transfer_record_type` (`type`),
                  KEY `ix_transfer_record_status` (`status`),
                  KEY `ix_transfer_record_created_at` (`created_at`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='交易记录';
                """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            await session.execute(text(create_biz_sql), execution_options={"warning": False})
