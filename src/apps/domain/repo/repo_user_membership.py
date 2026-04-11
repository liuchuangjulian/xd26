from js_kits.fastapi_kits.repo_base import BaseRepository
import warnings
from sqlalchemy import text

from apps.domain.entities.user_membership import UserMembershipEntity


class UserMembershipRepository(BaseRepository):
    async def ini(self, session):
        create_biz_sql = """
                CREATE TABLE IF NOT EXISTS `user_membership` (
                  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
                  `uid` bigint NOT NULL COMMENT '用户ID',
                  `membership_id` bigint NOT NULL COMMENT '会员ID',
                  `membership_info` json DEFAULT NULL COMMENT '会员信息快照',
                  `start_day` date NOT NULL COMMENT '开始日期',
                  `end_day` date NOT NULL COMMENT '结束日期',
                  `extend_property` json DEFAULT NULL COMMENT '扩展数据',
                  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                  `deleted_at` datetime DEFAULT NULL COMMENT '删除时间',
                  PRIMARY KEY (`id`),
                  KEY `ix_user_membership_uid` (`uid`),
                  KEY `ix_user_membership_end_day` (`end_day`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户会员信息';
                """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            await session.execute(text(create_biz_sql), execution_options={"warning": False})
