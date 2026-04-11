from js_kits.fastapi_kits.repo_base import BaseRepository
import warnings
from sqlalchemy import text


class CommunityRepository(BaseRepository):
    async def ini(self, session):
        create_biz_sql = """
                CREATE TABLE IF NOT EXISTS `community` (
                  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
                  `province` varchar(128) NOT NULL COMMENT '省',
                  `city` varchar(128) NOT NULL COMMENT '市',
                  `district` varchar(128) NOT NULL COMMENT '区',
                  `name` varchar(128) NOT NULL COMMENT '小区',
                  `lon` float DEFAULT NULL COMMENT '经度',
                  `lat` float DEFAULT NULL COMMENT '纬度',
                  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '数据更新时间',
                  `deleted_at` datetime DEFAULT NULL,
                  PRIMARY KEY (`id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='可选小区';
                """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            await session.execute(text(create_biz_sql), execution_options={"warning": False})
