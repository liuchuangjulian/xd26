from js_kits.fastapi_kits.repo_base import BaseRepository
import warnings
from sqlalchemy import text
from apps.domain.entities.config import ConfigEntity


class ConfigRepository(BaseRepository):
    async def ini(self, session):
        create_biz_sql = """
                CREATE TABLE IF NOT EXISTS `config` (
                  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
                  `key` varchar(64) NOT NULL COMMENT '名称',
                  `name` varchar(64) NOT NULL COMMENT '名称',
                  `is_active` tinyint NOT NULL COMMENT '是否生效：0未生效，1已生效',
                  `extend_property` json DEFAULT NULL COMMENT '属性信息',
                  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                  `deleted_at` datetime DEFAULT NULL COMMENT '删除时间',
                  PRIMARY KEY (`id`),
                  KEY `ix_config_key` (`key`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='配置表';
                """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            await session.execute(text(create_biz_sql), execution_options={"warning": False})

        _, obj_list = await self.get_list(session, Entity=ConfigEntity, equal_maps={"id": 1}, with_total=False,
                                          with_none_deleted=False)
        if not obj_list:
            await self.add(session, ConfigEntity(id=1, key="notice", name="提示：系统维护", is_active=0, extend_property={
                "show": 1,
                "title": "系统维护通知",
                "content": "系统将于2025年10月10日 23点开始进行停机维护，次日1点恢复服务。",
                "btn":
                {
                    "type": "one",
                    "text": "我知道了"
                }
            },deleted_at=None))
            await self.add(session, ConfigEntity(id=2, key="notice", name="提示：开通会员", is_active=1, extend_property= {
                    "show": 1,
                    "title": "开通会员提示",
                    "content": "本超市为会员专享超市，需开通会员后，购买。",
                    "btn":
                    {
                        "type": "two",
                        "text_ok": "去开通",
                        "text_ignore": "先看看"
                    }
                },deleted_at=None))

            await self.add(session,
                           ConfigEntity(id=3, key="weixin_kf", name="客服：微信列表", is_active=1, extend_property={
                               "wechat_id_list": ["weixin_0001", "weixin_0002", "weixin_0003"],
                           }, deleted_at=None))
