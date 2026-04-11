from fastapi_injector import Injected
from fastapi import APIRouter
import logging
from js_kits.fastapi_kits.user_route import UserRoute
from apps.use_case.shop.query_category import QueryCategory
from main.controllers.output.category import CategoryListResponse

router_category = APIRouter(route_class=UserRoute, prefix="/category", tags=["类别"])
logger = logging.getLogger(__name__)


@router_category.get("/list", response_model=CategoryListResponse)
async def get_category_list(use_case: QueryCategory = Injected(QueryCategory)):
    await use_case.query()
'''
curl -X 'GET' 'http://localhost:8080/api/category/list' | jq .
'''