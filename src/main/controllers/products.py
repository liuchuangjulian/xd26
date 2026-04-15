from fastapi_injector import Injected
from fastapi import APIRouter, Depends
import logging
from js_kits.fastapi_kits.input import PageParams
from js_kits.fastapi_kits.user_route import UserRoute
from apps.use_case.shop.query_product import QueryProducts
from main.controllers.input.products import QueryProductsParams
router_products = APIRouter(route_class=UserRoute, prefix="/products", tags=["产品"])
logger = logging.getLogger(__name__)


@router_products.get("/list")
async def get_products_list(page_params: PageParams = Depends(),
                            params: QueryProductsParams = Depends(),
                            use_case: QueryProducts = Injected(QueryProducts),
                            ):
    await use_case.query(params.category_id, params.name, page_size=page_params.page_size, page=page_params.page)

"""
curl -X 'GET' 'http://localhost:30010/api/products/list?page=1&page_size=10&category_id=1' -H 'accept: application/json' | jq .
"""
