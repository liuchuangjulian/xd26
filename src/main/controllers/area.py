from fastapi import APIRouter, Query
from fastapi_injector import Injected
import logging
from js_kits.fastapi_kits.user_route import UserRoute
from apps.use_case.area.query_area import QueryArea

router_area = APIRouter(route_class=UserRoute, prefix="/area", tags=["省市区"])
logger = logging.getLogger(__name__)


@router_area.get("/tree")
async def get_area_tree(use_case: QueryArea = Injected(QueryArea)):
    """获取省市区树形结构"""
    await use_case.query_tree()
'''
# 测试命令
curl -X 'GET' \
  'http://localhost:8080/api/area/tree' \
  -H 'accept: application/json' | jq .
'''
