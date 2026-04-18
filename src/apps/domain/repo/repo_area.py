from js_kits.fastapi_kits.repo_base import BaseRepository
from sqlalchemy import select, text
from apps.domain.entities.area import Area


class AreaRepository(BaseRepository):

    async def get_all_areas(self, session):
        """获取所有区域数据，不分页"""
        # 使用原生SQL查询
        result = await session.execute(
            text("SELECT * FROM area WHERE deleted_at IS NULL ORDER BY code")
        )
        return result.fetchall()

    async def ini(self, session):
        create_area_sql = """CREATE TABLE IF NOT EXISTS `area` (
              `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
              `code` varchar(20) NOT NULL COMMENT '区域代码',
              `name` varchar(50) NOT NULL COMMENT '区域名称',
              `parent_code` varchar(20) DEFAULT NULL COMMENT '父级区域代码',
              `level` int DEFAULT NULL COMMENT '层级(1省,2市,3区)',
              `deleted_at` datetime DEFAULT NULL COMMENT '删除时间',
              `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '数据产生时间',
              `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '数据更新时间',
              PRIMARY KEY (`id`),
              KEY `ix_area_code` (`code`),
              KEY `ix_area_parent_code` (`parent_code`),
              KEY `ix_area_level` (`level`)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='区域表';
        """
        await session.execute(text(create_area_sql))

        # 初始化省市区数据
        await self._init_area_data(session)

    async def _init_area_data(self, session):
        """初始化省市区测试数据"""
        # 检查是否已有数据
        result = await session.execute(text("SELECT COUNT(*) FROM area"))
        count = result.scalar()

        if count > 0:
            return  # 已有数据，不重复插入

        # 省份数据
        provinces = [
            ("110000", "北京市", None, 1),
            ("310000", "上海市", None, 1),
            ("440000", "广东省", None, 1),
            ("330000", "浙江省", None, 1),
            ("320000", "江苏省", None, 1),
        ]

        for code, name, parent_code, level in provinces:
            await session.execute(
                text("INSERT INTO area (code, name, parent_code, level) VALUES (:code, :name, :parent_code, :level)"),
                {"code": code, "name": name, "parent_code": parent_code, "level": level}
            )

        # 市数据
        cities = [
            # 广东省下的市
            ("440100", "广州市", "440000", 2),
            ("440300", "深圳市", "440000", 2),
            ("440400", "珠海市", "440000", 2),
            ("440600", "佛山市", "440000", 2),
            # 浙江省下的市
            ("330100", "杭州市", "330000", 2),
            ("330200", "宁波市", "330000", 2),
            # 江苏省下的市
            ("320100", "南京市", "320000", 2),
            ("320500", "苏州市", "320000", 2),
        ]

        for code, name, parent_code, level in cities:
            await session.execute(
                text("INSERT INTO area (code, name, parent_code, level) VALUES (:code, :name, :parent_code, :level)"),
                {"code": code, "name": name, "parent_code": parent_code, "level": level}
            )

        # 区数据
        districts = [
            # 广州市下的区
            ("440103", "荔湾区", "440100", 3),
            ("440104", "越秀区", "440100", 3),
            ("440105", "海珠区", "440100", 3),
            ("440106", "天河区", "440100", 3),
            ("440111", "白云区", "440100", 3),
            ("440112", "黄埔区", "440100", 3),
            ("440113", "番禺区", "440100", 3),
            ("440114", "花都区", "440100", 3),
            ("440115", "南沙区", "440100", 3),
            ("440117", "从化区", "440100", 3),
            ("440118", "增城区", "440100", 3),
            # 深圳市下的区
            ("440304", "福田区", "440300", 3),
            ("440305", "南山区", "440300", 3),
            ("440306", "宝安区", "440300", 3),
            ("440307", "龙岗区", "440300", 3),
            ("440308", "盐田区", "440300", 3),
            ("440309", "龙华区", "440300", 3),
            ("440310", "坪山区", "440300", 3),
            ("440311", "光明区", "440300", 3),
            # 杭州市下的区
            ("330102", "上城区", "330100", 3),
            ("330105", "拱墅区", "330100", 3),
            ("330106", "西湖区", "330100", 3),
            ("330108", "滨江区", "330100", 3),
            ("330109", "萧山区", "330100", 3),
            ("330110", "余杭区", "330100", 3),
            ("330111", "富阳区", "330100", 3),
            ("330112", "临安区", "330100", 3),
            # 南京市下的区
            ("320102", "玄武区", "320100", 3),
            ("320104", "秦淮区", "320100", 3),
            ("320105", "建邺区", "320100", 3),
            ("320106", "鼓楼区", "320100", 3),
            ("320111", "浦口区", "320100", 3),
            ("320113", "栖霞区", "320100", 3),
            ("320114", "雨花台区", "320100", 3),
            ("320115", "江宁区", "320100", 3),
            ("320116", "六合区", "320100", 3),
            # 苏州市下的区
            ("320505", "虎丘区", "320500", 3),
            ("320506", "吴中区", "320500", 3),
            ("320507", "相城区", "320500", 3),
            ("320508", "姑苏区", "320500", 3),
            ("320509", "吴江区", "320500", 3),
            ("320581", "常熟市", "320500", 3),
            ("320582", "张家港市", "320500", 3),
            ("320583", "昆山市", "320500", 3),
            ("320585", "太仓市", "320500", 3),
        ]

        for code, name, parent_code, level in districts:
            await session.execute(
                text("INSERT INTO area (code, name, parent_code, level) VALUES (:code, :name, :parent_code, :level)"),
                {"code": code, "name": name, "parent_code": parent_code, "level": level}
            )


