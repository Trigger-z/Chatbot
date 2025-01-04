import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

app = FastAPI()

# 图片路径
IMAGE_DIRECTORY = "Koharu"  # 假设图片存放在这个文件夹下


def get_image(image_name: str):
    """根据图片名称获取图片的二进制数据并返回"""
    try:
        # 拼接图片的完整路径
        image_path = os.path.join(IMAGE_DIRECTORY, image_name)

        # 检查文件是否存在
        if not os.path.exists(image_path):
            raise HTTPException(status_code=404, detail="Image not found")

        # 返回图片文件
        return FileResponse(image_path, media_type="image/png")  # 根据实际图片类型修改 media_type
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# 获取所有图片路径
def get_all_images():
    image_dir = "Koharu"
    image_list = []
    for root, _, files in os.walk(image_dir):
        for file in files:
            if file.endswith((".jpg", ".jpeg", ".png", ".gif")):
                image_path = os.path.join(root, file).replace("\\", "/")
                image_list.append(f"/{image_path}")
    return image_list

# 定义一个全局变量来保存图片列表和当前索引
image_list = get_all_images()
current_index = 0

# 获取下一张图片
def get_next_image():
    global current_index
    if not image_list:
        return None

    image = image_list[current_index]
    current_index = (current_index + 1) % len(image_list)
    return image
