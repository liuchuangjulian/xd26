import logging
from js_kits.except_kits.except_kits import FastapiResult
from apps.domain.repo.repo_area import AreaRepository

logger = logging.getLogger(__name__)


class QueryArea:
    def __init__(self, repo: AreaRepository, session=None):
        self.repo = repo
        self.session = session

    async def query_tree(self) -> None:
        """查询省市区树形结构"""
        from sqlalchemy import text

        # 使用repository的session
        async with self.repo.session as session:
            # 直接使用原生SQL查询所有区域
            result = await session.execute(
                text("SELECT code, name, parent_code, level FROM area WHERE deleted_at IS NULL ORDER BY code")
            )
            rows = result.fetchall()

            # 构建树形结构
            tree, _ = self._build_tree(rows)

            raise FastapiResult({
                "msg": "ok",
                "data": tree
            })

    def _build_tree(self, area_list):
        """构建树形结构"""
        if not area_list:
            return [], []

        # 处理Row对象或实体对象
        processed_list = []
        for item in area_list:
            # 检查对象类型
            if hasattr(item, '_fields'):
                # SQLAlchemy Row对象
                row_dict = {key: getattr(item, key) for key in item._fields}
                # 创建一个简单对象来存储数据
                class SimpleArea:
                    def __init__(self, data):
                        self.code = data.get('code')
                        self.name = data.get('name')
                        self.parent_code = data.get('parent_code')
                        self.level = data.get('level')
                    def to_dict(self):
                        return {
                            "code": self.code,
                            "name": self.name,
                            "parent_code": self.parent_code,
                            "level": self.level
                        }
                processed_list.append(SimpleArea(row_dict))
            elif hasattr(item, 'to_dict'):
                # 实体对象
                processed_list.append(item)
            else:
                # 未知对象类型，尝试直接访问属性
                processed_list.append(item)

        area_list = processed_list

        # 分离省份（level=1）
        provinces = [area for area in area_list if area.level == 1]

        # 构建树
        tree = []
        for province in provinces:
            # 查找该省份下的城市（level=2）
            cities = [area for area in area_list if area.parent_code == province.code and area.level == 2]

            if cities:
                # 有城市，构建省->市->区县的三级结构
                city_list = []
                for city in cities:
                    # 查找该城市下的区县
                    districts = [area for area in area_list if area.parent_code == city.code and area.level == 3]
                    district_list = [d.to_dict() for d in districts]

                    city_list.append({
                        **city.to_dict(),
                        "children": district_list
                    })

                tree.append({
                    **province.to_dict(),
                    "children": city_list
                })
            else:
                # 没有城市（直辖市），直接查找区县
                districts = [area for area in area_list if area.parent_code == province.code and area.level == 3]
                district_list = [d.to_dict() for d in districts]

                tree.append({
                    **province.to_dict(),
                    "children": district_list
                })

        return tree, []

    async def query_by_parent(self, parent_code: str = None) -> None:
        """根据父级编码查询区域列表"""
        async with self.repo.session as session:
            if parent_code:
                total, obj_list = await self.repo.get_list(
                    session,
                    equal_maps={"parent_code": parent_code},
                    with_total=False
                )
            else:
                # 查询省级
                total, obj_list = await self.repo.get_list(
                    session,
                    equal_maps={"level": 1},
                    with_total=False
                )

            raise FastapiResult({
                "msg": "ok",
                "data": [area.to_dict() for area in obj_list]
            })
