from pydantic import BaseModel
from typing import Optional, List
from main.controllers.pydantic_base.auto_title_field import AutoTitleField


class ProductDetail(BaseModel):
    p_id: int = AutoTitleField(..., description="商品ID")
    name: str = AutoTitleField(..., description="商品名称")
    img: str = AutoTitleField(..., description="商品图片")
    price: str = AutoTitleField(..., description="单价（元）")
    count: int = AutoTitleField(..., description="数量")
    subtotal: str = AutoTitleField(..., description="小计（元）")


class CouponInfo(BaseModel):
    id: int = AutoTitleField(..., description="优惠券ID")
    title: str = AutoTitleField(..., description="优惠券标题")
    discount: str = AutoTitleField(..., description="优惠金额（元）")


class PreCreateOrderData(BaseModel):
    products: List[ProductDetail] = AutoTitleField(..., description="商品列表")
    raw_total: str = AutoTitleField(..., description="商品总价（元）")
    delivery_fee: str = AutoTitleField(..., description="配送费（元）")
    discount: str = AutoTitleField(..., description="优惠金额（元）")
    total: str = AutoTitleField(..., description="最终总价（元）")
    coupon: Optional[CouponInfo] = AutoTitleField(None, description="最优优惠券信息")


class PreCreateOrderResponse(BaseModel):
    code: int = AutoTitleField(..., description="状态码")
    msg: str = AutoTitleField(..., description="信息")
    data: PreCreateOrderData = AutoTitleField(..., description="订单详情")
