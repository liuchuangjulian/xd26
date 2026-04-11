from js_kits.arequest.arequest import aio_request
# from js_kits.fastapi_kits.check_env import *
import os
import logging
from js_kits.fastapi_kits.import_into_env import dev_import
from js_kits.fastapi_kits.swagger import patch
from js_kits.fastapi_kits.app import create_fastapi_app
from main.controllers import router
from js_kits.fastapi_kits.log_conf import set_logging
from main.module import setup_dependency_injection
logger = logging.getLogger()
dev_import("../../config.yml")
patch()


async def do_ini():
    status, data = await aio_request(f'http://localhost:{os.getenv("PORT")}/api/ini')
    logger.info(f"do_ini status:{status},data:{data}")


def web_app():
    from apps.domain.orm_user import start_mappers as mapper_user
    from apps.domain.orm_shop import start_mappers as mapper_shop
    from apps.domain.orm_area import start_mappers as mapper_area
    from apps.domain.orm_redemption import start_mappers as mapper_redemption
    from apps.domain.orm_config import start_mappers as mapper_config

    mapper_shop()
    mapper_user()
    mapper_area()
    mapper_redemption()
    mapper_config()
    set_logging(logger, stream_level=os.getenv("LOG_LEVEL"))
    app = create_fastapi_app(setup_dependency_injection(), do_ini)
    app.include_router(router, prefix="")
    return app


if __name__ == "__main__":
    # pre_setting()
    import uvicorn
    port = os.getenv("PORT")
    # port = 8001
    server_name = os.getenv("SERVER_NAME")
    print(f"docs: http://localhost:{port}/{server_name}/docs")
    uvicorn.run("main.run:web_app", host="0.0.0.0", port=int(port), reload=True, log_level="error")

    # PYTHONUNBUFFERED=1;CONFIG_URL_SET_UP=http://localhost:23000/config/internal?key=xd25&cache=0
