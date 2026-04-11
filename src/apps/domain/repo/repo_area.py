from js_kits.fastapi_kits.repo_base import BaseRepository
from sqlalchemy import select, text
from apps.domain.entities.area import Area


class AreaRepository(BaseRepository):

    async def get_all_areas(self, session):
        """获取所有区域数据，不分页"""
        # 使用原生SQL查询
        result = await session.execute(
            text("SELECT * FROM area WHERE deleted_at IS NULL ORDER BY code")
        )
        return result.fetchall()


