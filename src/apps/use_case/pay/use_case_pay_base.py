import json
import logging
import os
from dataclasses import dataclass, asdict
from random import sample
from string import ascii_letters, digits
from wechatpayv3 import WeChatPay, WeChatPayType
from datetime import datetime
from js_kits.except_kits.except_kits import FastapiResult, BackendException

from apps.domain.entities.transfer_record import TransferRecord

logger = logging.getLogger(__name__)

QueryProductTypeCustomer = "customer"
QueryProductTypeBoss = "boss"


class UseCasePayBase:
    def __init__(self,  wx_pay: WeChatPay, repo: RecordRepository, uow: AsyncUnitOfWork):
        self.repo = repo
        self.wx_pay = wx_pay
        self.uow = uow


    async def save_transfer_record(self):
        obj = TransferRecord(type=RecordType.Recharge.value, shop_id=input_dto.user_obj.shop_id,
                     user_id=input_dto.user_obj.id, amount=input_dto.amount + gift,
                     real=input_dto.amount, gift=gift, status=RecordStatus.UnPay.value)
        await self.repo.add(obj)
        await self.repo.session.flush()
        out_trade_no = str(obj.id)
        while len(out_trade_no) < 6:
            out_trade_no = "0" + out_trade_no
        return obj.out_trade_no

    def prepay(self, description, out_trade_no, amount, user_obj):
        payer = {'openid': user_obj.openid}
        code, message = self.wx_pay.pay(
            description=description,
            out_trade_no=out_trade_no,
            amount={"total": amount},
            pay_type=WeChatPayType.JSAPI,
            payer=payer)
        logger.info(f"微信预支付 code:{code},message:{message}")
        result = json.loads(message)
        return code, result

    def to_client(self, code, result, out_trade_no):
        if code not in range(200, 300):
            return
        APPID = os.getenv("WX_APP_ID")
        prepay_id = result.get('prepay_id')
        dt = datetime.now()
        timestamp = str(int(datetime.timestamp(dt)))
        noncestr = ''.join(sample(ascii_letters + digits, 30))
        package = 'prepay_id=' + prepay_id
        paysign = self.wx_pay.sign([APPID, timestamp, noncestr, package])
        signtype = 'RSA'
        result_dict = {
            'appId': APPID,
            'timeStamp': timestamp,
            'nonceStr': noncestr,
            'package': 'prepay_id=%s' % prepay_id,
            'signType': signtype,
            'out_trade_no': out_trade_no,
            'paySign': paysign
        }
        raise FastapiResult({"msg": "ok",
                             "data": result_dict
                             })

    async def pay(self, session, description, amount, user_obj) -> None:
        # async with self.repo.session as session:
        # order_obj = await self.get_order_obj(order_id, session)
        out_trade_no = await self.save_transfer_record()
        code, result = self.prepay(description, out_trade_no, amount, user_obj)
        self.to_client(code, result, out_trade_no)
        raise BackendException()
