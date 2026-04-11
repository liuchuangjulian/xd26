import injector
from js_kits.fastapi_kits.async_injection_provider import async_provider
from apps.domain.repo.repo_config import ConfigRepository
from apps.use_case.notice.query_notice import QueryNotice


class NoticeModule(injector.Module):

    @async_provider
    async def get_query_notice(self, repo: ConfigRepository) -> QueryNotice:
        return QueryNotice(repo)
