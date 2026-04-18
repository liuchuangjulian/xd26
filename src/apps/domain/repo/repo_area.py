from js_kits.fastapi_kits.repo_base import BaseRepository
from sqlalchemy import select, text
from apps.domain.entities.area import Area


class AreaRepository(BaseRepository):

    async def get_all_areas(self, session):
        """获取所有区域数据，不分页"""
        # 使用原生SQL查询
        result = await session.execute(
            text("SELECT * FROM area WHERE deleted_at IS NULL ORDER BY code")
        )
        return result.fetchall()

    async def ini(self, session):
        create_area_sql = """CREATE TABLE IF NOT EXISTS `area` (
              `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
              `code` varchar(20) NOT NULL COMMENT '区域代码',
              `name` varchar(50) NOT NULL COMMENT '区域名称',
              `parent_code` varchar(20) DEFAULT NULL COMMENT '父级区域代码',
              `level` int DEFAULT NULL COMMENT '层级(1省,2市,3区)',
              `deleted_at` datetime DEFAULT NULL COMMENT '删除时间',
              `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '数据产生时间',
              `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '数据更新时间',
              PRIMARY KEY (`id`),
              KEY `ix_area_code` (`code`),
              KEY `ix_area_parent_code` (`parent_code`),
              KEY `ix_area_level` (`level`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='区域表';
        """
        await session.execute(text(create_area_sql))


