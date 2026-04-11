from js_kits.fastapi_kits.repo_base import BaseRepository
import warnings
from sqlalchemy import text


class OrderLineRepository(BaseRepository):
    async def ini(self, session):
        create_biz_sql = """
                CREATE TABLE IF NOT EXISTS `order_line` (
                  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
                  `uid` int DEFAULT NULL COMMENT 'uid',
                  `index` int DEFAULT NULL COMMENT '序号',
                  `name` varchar(128) NOT NULL COMMENT '品名',
                  `barcode` varchar(128) NOT NULL COMMENT '条码',
                  `order_id` int DEFAULT NULL COMMENT 'order_id',
                  `p_id` int DEFAULT NULL COMMENT '商品id',
                  `price` int DEFAULT NULL COMMENT '价格(单价格)',
                  `amount` int DEFAULT NULL COMMENT '总价格',
                  `count` int DEFAULT NULL COMMENT '商品数量',
                  `extend_property` json DEFAULT NULL COMMENT '扩展数据',
                  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '数据更新时间',
                  `deleted_at` datetime DEFAULT NULL,
                  PRIMARY KEY (`id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单行';
                """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            await session.execute(text(create_biz_sql), execution_options={"warning": False})
