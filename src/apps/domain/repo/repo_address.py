from js_kits.fastapi_kits.repo_base import BaseRepository
import warnings
from sqlalchemy import text

# from apps.domain.entities.user import User


class AddressRepository(BaseRepository):
    async def ini(self, session):
        create_biz_sql = """
                CREATE TABLE IF NOT EXISTS `address` (
                  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
                  `uid` bigint NOT NULL COMMENT 'uid',
                  `province` varchar(128) NOT NULL COMMENT 'province',
                  `city` varchar(128) NOT NULL COMMENT 'city',
                  `district` varchar(128) NOT NULL COMMENT 'district',
                  `community_name` varchar(128) NOT NULL COMMENT 'community_name',
                  `room` varchar(128) NOT NULL COMMENT '门牌，如：2013室',
                  `unit` varchar(128) NOT NULL COMMENT '单元',
                  `building` varchar(128) NOT NULL COMMENT '2号楼',
                  `phone` varchar(128) NOT NULL COMMENT '手机',
                  `name` varchar(128) NOT NULL COMMENT '联系人',
                  `selected` smallint NOT NULL COMMENT '选择',
                  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '数据更新时间',
                  `deleted_at` datetime DEFAULT NULL,
                  PRIMARY KEY (`id`),
                  KEY `ix_address_user_id` (`uid`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='地址';
                """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            await session.execute(text(create_biz_sql), execution_options={"warning": False})


