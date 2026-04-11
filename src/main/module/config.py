import injector
from js_kits.fastapi_kits.async_injection_provider import async_provider
from sqlalchemy.ext.asyncio import AsyncSession
from apps.domain.entities.config import ConfigEntity
from apps.domain.repo.repo_config import ConfigRepository


class ConfigModule(injector.Module):

    @async_provider
    async def get_config_repository(self, session: AsyncSession) -> ConfigRepository:
        return ConfigRepository(session=session, Entity=ConfigEntity)
