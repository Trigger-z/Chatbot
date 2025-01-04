from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from openai import OpenAI
import os
import logging
from dotenv import load_dotenv
import base64

from images import get_next_image
# 加载环境变量
load_dotenv()
# 设置路由
chat_router = APIRouter()

# 定义请求体模型
class Message(BaseModel):
    message: str

# 设置 OpenAI 客户端
api_key = os.getenv("API_KEY")
client = OpenAI(api_key=api_key)

# 聊天接口
@chat_router.post("/chat/")
async def chat(data: Message):
    logging.debug(f"Received message: {data.message}")

    try:
        # 调用 OpenAI 接口
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=[{"role": "user", "content": data.message}],
        )
        logging.debug(f"Received OpenAI response: {response}")

        # 获取下一张图片
        image_url = get_next_image()
        with open(image_url, "rb") as img_file:
            img_data = img_file.read()
            encoded_image = base64.b64encode(img_data).decode('utf-8')
        # 返回回复和图片路径
        return {
            "reply": response.choices[0].message.content,
            "image_data": encoded_image  # 返回 base64 编码的图片数据
        }

    except Exception as e:
        logging.error(f"Error during OpenAI request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"OpenAI request failed: {str(e)}")
