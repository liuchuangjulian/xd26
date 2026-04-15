import os
import uuid
from datetime import datetime
from typing import Optional
from fastapi import UploadFile, HTTPException
from js_kits.except_kits.except_kits import ClientError
import logging

logger = logging.getLogger(__name__)


# 允许的图片格式
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
# 最大文件大小 5MB
MAX_FILE_SIZE = 5 * 1024 * 1024
# 最小尺寸 200x200
MIN_IMAGE_SIZE = 200


async def validate_image_file(file: UploadFile) -> None:
    """验证上传的图片文件"""
    # 检查文件扩展名
    if not file.filename:
        raise ClientError({"msg": "文件名不能为空"})

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ClientError({"msg": f"不支持的文件格式，仅支持 {', '.join(ALLOWED_EXTENSIONS)}"})

    # 检查文件大小
    content = await file.read()
    await file.seek(0)  # 重置文件指针

    if len(content) > MAX_FILE_SIZE:
        raise ClientError({"msg": f"文件大小不能超过 {MAX_FILE_SIZE // 1024 // 1024}MB"})

    if len(content) == 0:
        raise ClientError({"msg": "文件不能为空"})


async def save_upload_file(
    file: UploadFile,
    user_id: int,
    upload_dir: str
) -> str:
    """
    保存上传的文件并返回访问URL（相对路径）

    Args:
        file: 上传的文件
        user_id: 用户ID
        upload_dir: 上传目录（相对于static目录）

    Returns:
        文件访问URL（相对路径）
    """
    await validate_image_file(file)

    # 生成唯一文件名：日期/用户ID_随机字符串.扩展名
    date_str = datetime.now().strftime("%Y%m%d")
    ext = os.path.splitext(file.filename)[1].lower()
    unique_str = uuid.uuid4().hex[:8]
    filename = f"{user_id}_{unique_str}{ext}"

    # 构建完整路径
    static_path = os.getenv("StaticPath")
    full_dir = os.path.join(static_path, upload_dir, date_str)
    full_path = os.path.join(full_dir, filename)

    # 创建目录
    os.makedirs(full_dir, exist_ok=True)

    # 保存文件
    try:
        content = await file.read()
        with open(full_path, "wb") as f:
            f.write(content)
    except Exception as e:
        logger.error(f"保存文件失败: {e}")
        raise ClientError({"msg": "文件保存失败"})

    # 返回相对路径URL
    file_url = f"/static/{upload_dir}/{date_str}/{filename}"
    logger.info(f"文件上传成功: {file_url}")
    return file_url
