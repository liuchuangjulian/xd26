from fastapi import APIRouter, Request, UploadFile, Depends
import logging
from js_kits.fastapi_kits.user_route import UserRoute
from apps.use_case.notice.query_notice import QueryNotice
from main.controllers.output.notices import NoticeResponse
from fastapi_injector import Injected


router_notices = APIRouter(route_class=UserRoute, prefix="", tags=["系统维护通知"])
logger = logging.getLogger(__name__)


@router_notices.get("/notices", response_model=NoticeResponse)
async def get_notices(query: QueryNotice = Injected(QueryNotice)):
    await query.query()

'''
curl -X 'GET' 'http://localhost:8080/api/notices' -H 'accept: application/json' | jq .
'''