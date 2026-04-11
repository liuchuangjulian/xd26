from fastapi import Request, Body
from fastapi import APIRouter, Body, Depends
from fastapi_injector import Injected
from wechatpayv3 import WeChatPay, WeChatPayType
# from apps.xiao_dao.repositories.entities.record import RecordStatus, Record
# from apps.xiao_dao.repositories.repo_order import OrderRepository
# from apps.xiao_dao.repositories.repo_record import RecordRepository
# from apps.xiao_dao.repositories.repo_shop import ShopRepository
# from apps.xiao_dao.repositories.repo_user import UserRepository
# from apps.xiao_dao.use_case.pay.recharge import Recharge, RechargeInputDto
# from lib.uow import AsyncUnitOfWork
# from lib.user_exception import FastapiResult, ClientError, UnauthorizedError
import logging

from main.controllers.input.pay import GetRecordParams

# from webapp.controllers.xd.input.pay.get_record import GetRecordParams
# from webapp.controllers.xd.input.pay.pay import PayParams, prepare_recharge_input
# from webapp.controllers.check_login import check_login, get_shop_obj

router_pay = APIRouter(prefix="", tags=["支付"])
logger = logging.getLogger(__name__)

# src/apps/xiao_dao/use_case/pay/recharge.py
@router_pay.post("/pay", summary="用户支付（线上充值）")
async def pay(
        request: Request,
        params: PayParams = Body(...),
        repo: UserRepository = Injected(UserRepository),
        shop_repo: ShopRepository = Injected(ShopRepository),
        recharge: Recharge = Injected(Recharge),
):
    request.state.request_body = await request.body()
    user_obj, shop_obj = await check_login(request, repo, shop_repo, params)
    out_dto = await recharge.execute(prepare_recharge_input(params, user_obj))

    raise FastapiResult(out_dto.to_dict())


@router_pay.post("/notify", summary="微信回调")
async def notify(
        request: Request,
        wx_pay: WeChatPay = Injected(WeChatPay),
        repo: RecordRepository = Injected(RecordRepository),
        user_repo: UserRepository = Injected(UserRepository),
        uow: AsyncUnitOfWork = Injected(AsyncUnitOfWork),
):
    request.state.request_body = await request.body()
    result = wx_pay.callback(request.headers, await request.body())
    if result and result.get('event_type') == 'TRANSACTION.SUCCESS':
        resp = result.get('resource')
        appid = resp.get('appid')
        mchid = resp.get('mchid')
        out_trade_no = resp.get('out_trade_no')
        transaction_id = resp.get('transaction_id')
        trade_type = resp.get('trade_type')
        trade_state = resp.get('trade_state')
        trade_state_desc = resp.get('trade_state_desc')
        bank_type = resp.get('bank_type')
        attach = resp.get('attach')
        success_time = resp.get('success_time')
        payer = resp.get('payer')
        amount = resp.get('amount').get('total')

        out_trade_no = str(int(out_trade_no))

        async with uow:
            record_obj = await repo.get_data_by_id(out_trade_no)
            if record_obj:
                record_obj.paid(amount)
                record_obj.extra = {
                    "appid": appid,
                    "mchid": mchid,
                    "transaction_id": transaction_id,
                    "trade_type": trade_type,
                    "trade_state": trade_state,
                    "trade_state_desc": trade_state_desc,
                    "bank_type": bank_type,
                    "attach": attach,
                    "success_time": success_time,
                    "payer": payer,
                    "amount": amount,
                }
                record_obj.set_modified()

                user_obj = await user_repo.get_data_by_id(record_obj.user_id)
                user_obj.recharge(record_obj)
                record_obj.record_add_to_user_time()

        logger.info(f"appid:{appid}, mchid:{mchid}, out_trade_no：{out_trade_no} transaction_id:{transaction_id}, "
                    f"trade_type{trade_type} trade_state{trade_state} trade_state_desc{trade_state_desc}"
                    f"bank_type{bank_type} attach{attach} success_time{success_time} payer{payer} amount{amount}")
        out_dto = {'code': 'SUCCESS', 'message': '成功'}
    else:
        out_dto = {'code': 'FAILED', 'message': '失败'}

    raise FastapiResult(out_dto)


@router_pay.post("/get_record", summary="获取充值结果")
async def get_record(
        request: Request,
        params: GetRecordParams = Body(...),
        # repo: UserRepository = Injected(UserRepository),
        # shop_repo: ShopRepository = Injected(ShopRepository),
        # record_repo: RecordRepository = Injected(RecordRepository),
):
    # query_transfer_record
    # request.state.request_body = await request.body()
    # user_obj, shop_obj = await check_login(request, repo, shop_repo, params)
    record_obj = await record_repo.get_data_by_id_user_id(params.record_id, str(user_obj.id))
    if record_obj:
        out_dto = {
            "code": 0,
            "msg": "ok",
            "result": record_obj.to_dict(),
        }
    else:
        out_dto = {
            "code": 1,
            "msg": "未查询到",
        }
    raise FastapiResult(out_dto)