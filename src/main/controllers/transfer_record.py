from aioredis import Redis
from fastapi_injector import Injected
from fastapi import APIRouter, Request, Depends, Body
import logging
from js_kits.fastapi_kits.user_route import UserRoute
from js_kits.fastapi_kits.input import PageParams
from apps.domain.repo.repo_user import UserRepository
from apps.use_case.pay.query_transfer_record import QueryTransferRecord
from main.controllers.check_auth import auth

router_transfer_record = APIRouter(route_class=UserRoute, prefix="/transfer-record", tags=["交易记录"])
logger = logging.getLogger(__name__)


@router_transfer_record.get("/list")
@auth
async def get_transfer_record_list(
        request: Request,
        redis_client: Redis = Injected(Redis),
        user_repo: UserRepository = Injected(UserRepository),
        uid=None,
        page_params: PageParams = Depends(),
        status: str = None,
        use_case: QueryTransferRecord = Injected(QueryTransferRecord),
):
    await use_case.query(uid, status, page_params.page, page_params.page_size)
'''
curl -X 'GET' 'http://localhost:8080/api/transfer-record/list?page=1&page_size=10&status=paid' -H 'token: 7539b33b-a066-4dbc-b90c-f1f038fa429b' | jq .
'''