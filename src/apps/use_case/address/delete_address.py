import logging
from js_kits.except_kits.except_kits import FastapiResult, ClientError
from apps.domain.repo.repo_address import AddressRepository

logger = logging.getLogger(__name__)


class UseCaseDeleteAddress:
    def __init__(self, repo: AddressRepository):
        self.repo = repo

    async def execute(self, uid, address_id) -> None:
        async with self.repo.session as session:
            _, obj_list = await self.repo.get_list(session, equal_maps={"id": address_id, "uid": uid},
                                                   with_total=False)
            if not obj_list:
                raise ClientError({"msg": "id 不存在或者已经删除"})
            obj = obj_list[0]
            obj.delete()
            await self.repo.add(session, obj)
            raise FastapiResult({"msg": "ok"})
