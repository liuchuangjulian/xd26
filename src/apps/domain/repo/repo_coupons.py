import datetime

from js_kits.fastapi_kits.repo_base import BaseRepository
import warnings
from sqlalchemy import text

from apps.domain.entities.coupons import Coupon


class CouponsRepository(BaseRepository):
    async def ini(self, session):
        create_biz_sql = """
                CREATE TABLE IF NOT EXISTS `coupon` (
                  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
                  `coupon_type` smallint DEFAULT NULL COMMENT '类型',
                  `generated_type` smallint DEFAULT NULL COMMENT '类型',
                  `title` varchar(128) NOT NULL COMMENT '名字',
                  `price` int DEFAULT NULL COMMENT '价格',
                  `limit` int DEFAULT NULL COMMENT '限制',
                  `uid` bigint unsigned DEFAULT NULL COMMENT '用户id',
                  `extend_property` json DEFAULT NULL COMMENT '扩展属性',
                  `effected_at` date NOT NULL COMMENT '生效于',
                  `expired_at` date NOT NULL COMMENT '过期于',
                  `deleted_at` datetime DEFAULT NULL COMMENT '删除时间',
                  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '数据产生时间',
                  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '数据更新时间',
                  PRIMARY KEY (`id`),
                  KEY `ix_coupon_uid` (`uid`),
                  KEY `ix_coupon_effected_at` (`effected_at`),
                  KEY `ix_coupon_expired_at` (`expired_at`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='优惠券';
                 """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            await session.execute(text(create_biz_sql), execution_options={"warning": False})
        _, obj_list = await self.get_list(session, Entity=Coupon, equal_maps={"id": 1}, with_total=False,
                                          with_none_deleted=False)
        if not obj_list:
            await self.add(session, Coupon(id=1, coupon_type=1, generated_type=1, title="运费优惠券", price=600,
                                           limit=-1, uid=1, effected_at=datetime.datetime(year=2025, month=10, day=1),
                                           expired_at=datetime.datetime(year=2027, month=9, day=30),
                                           ))
