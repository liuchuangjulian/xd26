import logging
import datetime
from js_kits.except_kits.except_kits import FastapiResult
from apps.domain.entities.address import Address
from apps.domain.repo.repo_address import AddressRepository

logger = logging.getLogger(__name__)


class UseCaseCreateAddress:
    def __init__(self, repo: AddressRepository):
        self.repo = repo

    async def execute(self, uid, province, city, district,
                      community_name, building_unit_room, phone, name, selected, tag="") -> None:
        async with self.repo.session as session:
            if selected:
                _, address_list = await self.repo.get_list(session,
                                                           equal_maps={"uid": uid, "selected": 1},
                                                           with_total=False)
                if address_list:
                    for obj in address_list:
                        obj.selected = 0
                    await self.repo.add_all(session, address_list)

            obj = Address(uid=uid,
                          province=province, city=city, district=district,
                          community_name=community_name, building_unit_room=building_unit_room,
                          phone=phone, name=name, selected=selected, tag=tag,
                          created_at=datetime.datetime.now(), updated_at=datetime.datetime.now(),
                          deleted_at=None)
            await self.repo.add(session, obj)

            raise FastapiResult({"msg": "ok",
                                 "data": obj.id
                                 })
