from js_kits.fastapi_kits.repo_base import BaseRepository
import warnings
from sqlalchemy import text


class MembershipOrderRepository(BaseRepository):
    async def ini(self, session):
        create_biz_sql = """
                CREATE TABLE IF NOT EXISTS `membership_order` (
                  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
                  `uid` bigint NOT NULL COMMENT '用户ID',
                  `membership_id` bigint NOT NULL COMMENT '会员类型ID',
                  `out_trade_no` varchar(64) NOT NULL COMMENT '商户订单号',
                  `transaction_id` varchar(64) DEFAULT NULL COMMENT '微信支付订单号',
                  `total_fee` int NOT NULL COMMENT '订单金额（分）',
                  `status` tinyint NOT NULL DEFAULT 0 COMMENT '订单状态：0-未支付，1-已支付，2-已取消，3-已退款',
                  `membership_info` json DEFAULT NULL COMMENT '会员信息快照',
                  `pay_time` datetime DEFAULT NULL COMMENT '支付时间',
                  `extend_property` json DEFAULT NULL COMMENT '扩展数据',
                  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
                  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
                  `deleted_at` datetime DEFAULT NULL COMMENT '删除时间',
                  PRIMARY KEY (`id`),
                  UNIQUE KEY `ix_membership_order_out_trade_no` (`out_trade_no`),
                  KEY `ix_membership_order_uid` (`uid`),
                  KEY `ix_membership_order_status` (`status`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='会员购买订单';
                """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            await session.execute(text(create_biz_sql), execution_options={"warning": False})
