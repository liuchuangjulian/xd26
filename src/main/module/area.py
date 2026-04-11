import injector
from js_kits.fastapi_kits.async_injection_provider import async_provider
from sqlalchemy.ext.asyncio import AsyncSession
from apps.domain.entities.area import Area
from apps.domain.repo.repo_area import AreaRepository
from apps.use_case.area.query_area import QueryArea


class AreaModule(injector.Module):

    @async_provider
    async def provide_area_repository(self, session: AsyncSession) -> AreaRepository:
        return AreaRepository(session=session, Entity=Area)

    @async_provider
    async def provide_query_area(self, repo: AreaRepository) -> QueryArea:
        return QueryArea(repo=repo)
