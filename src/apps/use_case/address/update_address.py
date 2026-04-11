import logging
from js_kits.except_kits.except_kits import FastapiResult, ClientError
from apps.domain.repo.repo_address import AddressRepository

logger = logging.getLogger(__name__)


class UseCaseUpdateAddress:
    def __init__(self, repo: AddressRepository):
        self.repo = repo

    async def execute(self, address_id, uid,
                      province, city, district,
                      community_name, building_unit_room, phone, name, selected, tag="") -> None:
        async with self.repo.session as session:
            _, obj_list = await self.repo.get_list(session, equal_maps={"id": address_id, "uid": uid},
                                                   with_total=False)
            if not obj_list:
                raise ClientError({"msg": "id 不存在或者已经删除"})

            if selected:
                _, address_list = await self.repo.get_list(session,
                                                           equal_maps={"uid": uid, "selected": 1},
                                                           with_total=False)
                if address_list:
                    for obj in address_list:
                        obj.selected = 0
                    await self.repo.add_all(session, address_list)

            obj = obj_list[0]
            obj.update_all(**{"community_id": community_name,
                              "building_unit_room": building_unit_room,
                            "province": province, "city": city, "district": district,
                              "selected": selected,
                            "phone": phone, "name": name, "tag": tag})
            await self.repo.add(session, obj)
            raise FastapiResult({"msg": "ok"})
