from openai import OpenAI
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 创建 FastAPI 应用实例
app = FastAPI()

# 配置 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# 配置日志
logging.basicConfig(level=logging.DEBUG)

# 定义请求体的数据模型
class Message(BaseModel):
    message: str

# 设置 OpenAI 客户端
api_key = os.getenv("API_KEY")
client = OpenAI(api_key=api_key)

# 创建聊天接口
@app.post("/chat/")
async def chat(data: Message):
    # 打印收到的消息
    logging.debug(f"Received message: {data.message}")

    try:
        # 调用 gpt-4o-mini 模型
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,  # 如果该模型需要这个参数
            messages=[{"role": "user", "content": data.message}],
        )
        logging.debug(f"Received OpenAI response: {response}")
        # 提取回复并返回
        return {"reply": response.choices[0].message.content}

    except Exception as e:
        logging.error(f"Error during OpenAI request: {str(e)}")
        raise HTTPException(status_code=500, detail=f"OpenAI request failed: {str(e)}")
