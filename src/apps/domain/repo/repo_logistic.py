from js_kits.fastapi_kits.repo_base import BaseRepository
import warnings
from sqlalchemy import text

from apps.domain.entities.logistic import Logistic


class LogisticRepository(BaseRepository):
    async def ini(self, session):
        create_biz_sql = """
                CREATE TABLE IF NOT EXISTS `logistic` (
                      `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
                      `order_id` bigint unsigned DEFAULT NULL COMMENT '订单id',
                      `nodes` json DEFAULT NULL COMMENT '节点',
                      `status` smallint DEFAULT NULL COMMENT '当前状态',
                      `address_id` bigint unsigned DEFAULT NULL COMMENT '原始送货地址',
                      `address_info` json DEFAULT NULL COMMENT '地址快照',
                      `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '数据产生时间',
                      `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '数据更新时间',
                      PRIMARY KEY (`id`),
                      KEY `ix_logistic_status` (`status`),
                      KEY `ix_logistic_address_id` (`address_id`),
                      KEY `ix_logistic_order_id` (`order_id`)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单配送信息';
                """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            await session.execute(text(create_biz_sql), execution_options={"warning": False})

        _, obj_list = await self.get_list(session, Entity=Logistic, equal_maps={"id": 1}, with_total=False,
                                          with_none_deleted=False)
        if not obj_list:
            await self.add(session, Logistic(id=1, order_id=1, nodes=[{"name": "拣货中", "owner": "拣货员：xxx", "time": "2025-10-10 10:10:10", "phone": "021-12345678", "notes": ""}, {"name": "待出库", "owner": "出库员：xxx", "time": "2025-10-10 10:10:10", "phone": "021-12345678", "notes": ""}],status=1, address_id=1, address_info={}))
