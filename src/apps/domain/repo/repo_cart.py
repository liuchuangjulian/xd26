from js_kits.fastapi_kits.repo_base import BaseRepository
import warnings
from sqlalchemy import text


class CartRepository(BaseRepository):
    async def ini(self, session):
        create_biz_sql = """
                CREATE TABLE IF NOT EXISTS `cart` (
                  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
                  `uid` int DEFAULT NULL COMMENT 'uid',
                  `p_id_info_map` json DEFAULT NULL COMMENT '产品&数量',
                  `p_list` json DEFAULT NULL COMMENT '产品&数量',
                  `extend_property` json DEFAULT NULL COMMENT '扩展数据',
                  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '数据更新时间',
                  `deleted_at` datetime DEFAULT NULL,
                  PRIMARY KEY (`id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='购物车';
                """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            await session.execute(text(create_biz_sql), execution_options={"warning": False})
