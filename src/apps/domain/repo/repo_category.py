from js_kits.fastapi_kits.repo_base import BaseRepository
import warnings
from sqlalchemy import text

from apps.domain.entities.category import CategoryEntity


class CategoryRepository(BaseRepository):
    async def ini(self, session):
        create_biz_sql = """
                CREATE TABLE IF NOT EXISTS `category` (
                  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
                  `name` varchar(128) NOT NULL COMMENT '名称',
                  `show_index` int DEFAULT NULL COMMENT '展示序号',
                  `extend_property` json DEFAULT NULL COMMENT '扩展数据',
                  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '数据更新时间',
                  `deleted_at` datetime DEFAULT NULL,
                  PRIMARY KEY (`id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='类目';
                """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            await session.execute(text(create_biz_sql), execution_options={"warning": False})

        _, obj_list = await self.get_list(session, Entity=CategoryEntity, equal_maps={"id": 1}, with_total=False)
        if not obj_list:
            await self.add(session, CategoryEntity(id=1, name="饮料", show_index=1, extend_property={}))
            await self.add(session, CategoryEntity(id=2, name="酒", show_index=1, extend_property={}))
            await self.add(session, CategoryEntity(id=3, name="日化", show_index=1, extend_property={}))
            await self.add(session, CategoryEntity(id=4, name="方便速食", show_index=1, extend_property={}))
            await self.add(session, CategoryEntity(id=5, name="休闲食品", show_index=1, extend_property={}))
            await self.add(session, CategoryEntity(id=6, name="饮用水", show_index=1, extend_property={}))
            await self.add(session, CategoryEntity(id=7, name="家用", show_index=1, extend_property={}))
