from js_kits.fastapi_kits.repo_base import BaseRepository
import warnings
from sqlalchemy import text

from apps.domain.entities.membership import MembershipEntity


class MembershipRepository(BaseRepository):
    async def ini(self, session):
        create_biz_sql = """
                CREATE TABLE IF NOT EXISTS `membership` (
                  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
                  `name` varchar(128) NOT NULL COMMENT '会员名称',
                  `price` decimal(10,2) NOT NULL COMMENT '价格',
                  `duration` int NOT NULL COMMENT '有效期（天）',
                  `description` varchar(512) DEFAULT NULL COMMENT '描述',
                  `status` tinyint NOT NULL DEFAULT 1 COMMENT '状态：1-启用，0-禁用',
                  `show_index` int DEFAULT NULL COMMENT '展示序号',
                  `extend_property` json DEFAULT NULL COMMENT '扩展数据',
                  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '数据更新时间',
                  `deleted_at` datetime DEFAULT NULL,
                  PRIMARY KEY (`id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='会员信息';
                """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            await session.execute(text(create_biz_sql), execution_options={"warning": False})

        # 初始化一些示例数据
        _, obj_list = await self.get_list(session, Entity=MembershipEntity, with_total=False)
        if not obj_list:
            await self.add(session, MembershipEntity(
                id=1,
                name="月度会员",
                price=29.90,
                duration=30,
                description="享受30天会员权益",
                status=1,
                show_index=1,
                extend_property={}
            ))
            await self.add(session, MembershipEntity(
                id=2,
                name="季度会员",
                price=79.90,
                duration=90,
                description="享受90天会员权益，更划算",
                status=1,
                show_index=2,
                extend_property={}
            ))
            await self.add(session, MembershipEntity(
                id=3,
                name="年度会员",
                price=299.90,
                duration=365,
                description="享受365天会员权益，超值优惠",
                status=1,
                show_index=3,
                extend_property={}
            ))
