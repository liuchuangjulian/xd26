from js_kits.fastapi_kits.repo_base import BaseRepository
import warnings
from sqlalchemy import text

from apps.domain.entities.products import ProductsEntity


class ProductRepository(BaseRepository):
    async def ini(self, session):
        create_biz_sql = """
                CREATE TABLE IF NOT EXISTS `products` (
                  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
                  `category_id_list` json DEFAULT NULL COMMENT '类目列表',
                  `show_index` int DEFAULT NULL COMMENT '展示序号',
                  `name` varchar(128) NOT NULL COMMENT '名称',
                  `describe` varchar(1024) NOT NULL COMMENT '描述',
                  `barcode` varchar(128) NOT NULL COMMENT '条码',
                  `tips` json DEFAULT NULL COMMENT '提示列表',
                  `sold` int DEFAULT NULL COMMENT '提示列表',
                  `img` varchar(1024) NOT NULL COMMENT '主图',
                  `original_price` int NOT NULL COMMENT '原价',
                  `price` int NOT NULL COMMENT '售卖-价格',
                  `units` varchar(128) NOT NULL COMMENT '单位',
                  `extend_property` json DEFAULT NULL COMMENT '扩展数据',
                  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
                  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '数据更新时间',
                  `deleted_at` datetime DEFAULT NULL,
                  PRIMARY KEY (`id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品';
                """
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            await session.execute(text(create_biz_sql), execution_options={"warning": False})

        _, obj_list = await self.get_list(session, Entity=ProductsEntity, equal_maps={"id": 1}, with_total=False)
        if not obj_list:
            try:
                await self.add(session, ProductsEntity(id=1, name="红牛", show_index=1, category_id_list=[1],
                                                       barcode="1234567", tips={}, sold=1,
                                                       img="https://xd8.oss-cn-shanghai.aliyuncs.com/for_test_img.png",
                                                       original_price=600, price=500, units="瓶", describe="描述信息",
                                                       extend_property={}))
            except Exception as e:
                ...