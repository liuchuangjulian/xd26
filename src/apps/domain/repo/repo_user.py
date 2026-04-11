import datetime
from js_kits.fastapi_kits.repo_base import BaseRepository
from sqlalchemy import select, and_, or_
from typing import Optional, List
from apps.domain.entities.user import User
from apps.domain.entities.user_token import UserToken
from sqlalchemy.future import select
from sqlalchemy.sql.expression import cast
from sqlalchemy.dialects.postgresql import JSONB
import warnings
from sqlalchemy import text


class UserRepository(BaseRepository):
    async def add_token(self, session, obj: UserToken) -> bool:
        return await super().add(session, obj)

    async def get_user_info_by_open_id(self, session, scope: str, open_id: str) -> Optional[User]:
        stmt = select(User).where(cast(User.extend_property["wechat_openid"][scope], JSONB) == open_id)
        result = await session.execute(stmt)
        obj = result.scalars().first()
        return obj if obj and obj.get_scope_openid(scope) == open_id else None

    async def get_user_info_by_id(self, session, id: int) -> Optional[User]:
        stmt = select(User).where(User.id == id)
        result = await session.execute(stmt)
        return result.scalars().first()

    async def get_user_info_by_token(self, session, token: str) -> Optional[UserToken]:
        stmt = select(UserToken).where(and_(UserToken.token == token,
                                            UserToken.expired_at > datetime.datetime.now()))
        result = await session.execute(stmt)
        return result.scalars().first()

    async def get_token_by_uid(self, session, uid: int) -> List[str]:
        stmt = select(UserToken).where(and_(UserToken.uid == uid,
                                            UserToken.expired_at > datetime.datetime.now()))
        result = await session.execute(stmt)
        return [obj.token for obj in result.scalars().all()]

    async def ini(self, session):
        create_user_sql = """CREATE TABLE IF NOT EXISTS  `user` (
                  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
                  `nickname` varchar(32) DEFAULT NULL COMMENT '昵称',
                  `extend_property` json DEFAULT NULL COMMENT '扩展属性',
                  `phone` varchar(100) DEFAULT NULL COMMENT '加密手机号',
                  `wechat_openid` varchar(100) DEFAULT NULL COMMENT '微信openid',
                  `black` tinyint(4) DEFAULT NULL COMMENT '黑名单',
                  `avatar` varchar(1024) DEFAULT NULL COMMENT '头像',
                  `birthday` date DEFAULT NULL COMMENT '生日',
                  `deleted_at` datetime DEFAULT NULL COMMENT '删除时间',
                  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '数据产生时间',
                  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '数据更新时间',
                  PRIMARY KEY (`id`),
                  KEY `ix_user_black` (`black`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户';
                """
        create_user_token_sql = """CREATE TABLE IF NOT EXISTS `user_token` (
                      `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
                      `uid` bigint unsigned DEFAULT NULL COMMENT '用户id',
                      `token` varchar(100) NOT NULL COMMENT 'token',
                      `expired_at` datetime NOT NULL COMMENT '过期于',
                      `deleted_at` datetime DEFAULT NULL COMMENT '删除时间',
                      PRIMARY KEY (`id`),
                      KEY `ix_user_token_uid` (`uid`),
                      KEY `ix_user_token_expired_at` (`expired_at`),
                      KEY `ix_user_token_token` (`token`)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='token表';
        """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            await session.execute(text(create_user_sql), execution_options={"warning": False})
            await session.execute(text(create_user_token_sql), execution_options={"warning": False})

        _, obj_list = await self.get_list(session, Entity=User, equal_maps={"id": 1}, with_total=False)
        if not obj_list:
            await self.add(session, User(id=1,
                                         nickname="会员23320-55158",
                                         extend_property={},
                                         phone="",
                                         wechat_openid="-",
                                         black=0,
                                         avatar="",))
            await self.add(session, UserToken(id=1,
                                              uid=1,
                                              token="7539b33b-a066-4dbc-b90c-f1f038fa429b",
                                              expired_at=datetime.datetime.now()+datetime.timedelta(days=365),))
