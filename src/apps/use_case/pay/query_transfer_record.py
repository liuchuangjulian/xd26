import logging
from js_kits.except_kits.except_kits import FastapiResult
from apps.domain.repo.repo_transfer_record import TransferRecordRepository

logger = logging.getLogger(__name__)


class QueryTransferRecord:
    def __init__(self, repo: TransferRecordRepository):
        self.repo = repo

    async def query(self, uid, status, page, page_size) -> None:
        equal_maps = {"user_id": uid}

        if status:
            equal_maps["status"] = status

        async with self.repo.session as session:
            total, record_list = await self.repo.get_list(
                session,
                page=page,
                page_size=page_size,
                equal_maps=equal_maps,
                order_by_list=["created_at"],
                # order_by_desc=True
            )
            raise FastapiResult({"msg": "ok",
                                 "total": total,
                                 "page": page,
                                 "page_size": page_size,
                                 "data": [record_obj.to_dict() for record_obj in record_list]
                                 })
