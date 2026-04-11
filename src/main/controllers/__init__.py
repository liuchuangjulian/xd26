import os
from fastapi import APIRouter
from main.controllers.address import router_address
from main.controllers.area import router_area
from main.controllers.cart import router_cart
from main.controllers.coupons import router_coupons
from main.controllers.health import health_router
from main.controllers.category import router_category
from main.controllers.ini import router_api_ini
from main.controllers.logistic import router_logistic
from main.controllers.membership import router_membership
from main.controllers.notices import router_notices
from main.controllers.order import router_order
from main.controllers.products import router_products
from main.controllers.redemption import router_redemption
from main.controllers.transfer_record import router_transfer_record
from main.controllers.user import router_user

__all__ = ["router"]


server_name = os.getenv("SERVER_NAME")
router = APIRouter()

router.include_router(router_notices, prefix=f"/api")
router.include_router(router_user, prefix=f"/api")
router.include_router(router_area, prefix=f"/api")
router.include_router(router_redemption, prefix=f"/api")
router.include_router(router_category, prefix=f"/api")
router.include_router(router_products, prefix=f"/api")
router.include_router(router_cart, prefix=f"/api")
router.include_router(router_address, prefix=f"/api")
router.include_router(router_coupons, prefix=f"/api")
router.include_router(router_order, prefix=f"/api")
router.include_router(router_logistic, prefix=f"/api")
router.include_router(router_membership, prefix=f"/api")
router.include_router(router_transfer_record, prefix=f"/api")
router.include_router(router_api_ini, prefix=f"/api")
router.include_router(health_router, prefix=f"/api")