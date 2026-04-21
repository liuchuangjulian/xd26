from js_kits.fastapi_kits.repo_base import BaseRepository
import warnings
from sqlalchemy import text


class OrderRepository(BaseRepository):
    async def ini(self, session):
        create_biz_sql = """
                CREATE TABLE IF NOT EXISTS `order` (
                  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
                  `main_info` varchar(128) COMMENT '主要信息',
                  `uid` int DEFAULT NULL COMMENT 'uid',
                  `real_pay` int DEFAULT NULL COMMENT '实际支付',
                  `total` int DEFAULT NULL COMMENT '总金额',
                  `count` int DEFAULT NULL COMMENT '总件数',
                  `discount` int DEFAULT NULL COMMENT '总折扣',
                  `status` int NOT NULL COMMENT '状态',
                  `balance` int DEFAULT NULL COMMENT '余额',
                  `coins` int DEFAULT NULL COMMENT '使用积分',
                  `coupon_id_list` json DEFAULT NULL COMMENT '优惠券 id 数组',
                  `payment_id_list` json DEFAULT NULL COMMENT '支付id列表数组',
                  `delivery_id_list` json DEFAULT NULL COMMENT '配送id列表 数组',
                  `feedback_coins` int DEFAULT NULL COMMENT '回馈积分',
                  `out_trade_no` varchar(64) DEFAULT NULL COMMENT '商户订单号',
                  `transaction_id` varchar(64) DEFAULT NULL COMMENT '微信支付订单号',
                  `pay_time` datetime DEFAULT NULL COMMENT '支付时间',
                  `extend_property` json DEFAULT NULL COMMENT '扩展数据',
                  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '数据更新时间',
                  `deleted_at` datetime DEFAULT NULL,
                  PRIMARY KEY (`id`),
                  UNIQUE KEY `ix_order_out_trade_no` (`out_trade_no`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单';
                """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            await session.execute(text(create_biz_sql), execution_options={"warning": False})

