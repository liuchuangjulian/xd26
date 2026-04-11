import injector
from js_kits.fastapi_kits.async_injection_provider import async_provider
from sqlalchemy.ext.asyncio import AsyncSession
from apps.domain.entities.address import Address
from apps.domain.entities.transfer_record import TransferRecord
from apps.domain.repo.repo_address import AddressRepository
from apps.domain.repo.repo_transfer_record import TransferRecordRepository
from apps.use_case.pay.query_transfer_record import QueryTransferRecord
import os
from wechatpayv3 import WeChatPay, WeChatPayType


class PayModule(injector.Module):
    # pay.py

    # @injector.provider
    # def get_wx_api_repo(self) -> ApiWxRepository:
    #     return ApiWxRepository(None)

    @injector.singleton
    @injector.provider
    def get_wxpay(self) -> WeChatPay:
        # 微信支付商户号，服务商模式下为服务商户号，即官方文档中的sp_mchid。
        MCHID = os.getenv("MCHID")
        # 商户证书私钥，此文件不要放置在下面设置的CERT_DIR目录里。
        with open(os.getenv("APICLIENT_KEY")) as f:
            PRIVATE_KEY = f.read()
        # 商户证书序列号
        CERT_SERIAL_NO = os.getenv("APICLIENT_CERT")
        # API v3密钥， https://pay.weixin.qq.com/wiki/doc/apiv3/wechatpay/wechatpay3_2.shtml
        APIV3_KEY = os.getenv("APIV3_KEY")
        # APPID，应用ID，服务商模式下为服务商应用ID，即官方文档中的sp_appid，也可以在调用接口的时候覆盖。
        APPID = os.getenv("WX_APP_ID")
        # 回调地址，也可以在调用接口的时候覆盖。  'https://www.lijusheng.top/xd/notify'
        NOTIFY_URL = os.getenv("NOTIFY_URL")

        # 微信支付平台证书缓存目录，初始调试的时候可以设为None，首次使用确保此目录为空目录。
        CERT_DIR = './cert'

        # # 日志记录器，记录web请求和回调细节，便于调试排错。
        # logging.basicConfig(filename=os.path.join(os.getcwd(), 'demo.log'), level=logging.DEBUG, filemode='a',
        #                     format='%(asctime)s - %(process)s - %(levelname)s: %(message)s')
        # LOGGER = logging.getLogger("demo")

        # 接入模式：False=直连商户模式，True=服务商模式。
        PARTNER_MODE = False
        # 代理设置，None或者{"https": "http://10.10.1.10:1080"}，详细格式参见https://docs.python-requests.org/zh_CN/latest/user/advanced.html
        PROXY = None
        return WeChatPay(
            wechatpay_type=WeChatPayType.NATIVE,
            mchid=MCHID,
            private_key=PRIVATE_KEY,
            cert_serial_no=CERT_SERIAL_NO,
            apiv3_key=APIV3_KEY,
            appid=APPID,
            notify_url=NOTIFY_URL,
            cert_dir=CERT_DIR,
            # logger=LOGGER,
            partner_mode=PARTNER_MODE,
            proxy=PROXY)

    @async_provider
    async def get_transfer_record_repository(self, session: AsyncSession) -> TransferRecordRepository:
        return TransferRecordRepository(session=session, Entity=TransferRecord)

    @async_provider
    async def get_query_transfer_record(self, repo: TransferRecordRepository) -> QueryTransferRecord:
        return QueryTransferRecord(repo)
