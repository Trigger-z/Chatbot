import uvicorn
from openai import OpenAI
import logging
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from fastapi import FastAPI,Header,Body,Request
from fastapi.responses import JSONResponse,HTMLResponse,FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from chat import chat_router
from images import get_image
# 导入拆分的路由
import chat
import images

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
#logging.basicConfig(level=logging.DEBUG)

# 配置模板路径
templates = Jinja2Templates(directory="templates")

# 定义请求体的数据模型
class Message(BaseModel):
    message: str

# 挂载 Koharu 文件夹作为静态文件
app.mount("/Koharu", StaticFiles(directory="Koharu"), name="Koharu")

# 注册聊天路由
app.include_router(chat_router)
@app.get("/")
def index(username,req:Request):
      return templates.TemplateResponse("index.html",context={"request":req,"name":username})
@app.post("/login")
def login(data:dict=Body(None)):
    return {"data":data}
@app.api_route("/signin",methods=("get","post","put"))
def signin():
    return {"msg":"signin sucess"}
@app.get("/user")
def user(id,token=Header(None)):
    return {"id":id,"token":token}
@app.get("/get_image/{image_name}")
async def get_image_route(image_name: str):
    """处理请求并返回图片"""
    return get_image(image_name)

@app.get("/user1")
def user1():
    return JSONResponse(content={"msg":"user"},status_code=202,headers={"name":"aaa"})
@app.get("/user2")
def user2():
    html_content = """
    <html>
        <body><p style="color:red">Hello world</p></body>
    </html>
    """
    return HTMLResponse(content=html_content,status_code=202,headers={"name":"aaa"})
@app.get("/user3")
def user3():
    avatar = "Koharu/1.png"
    return FileResponse(avatar,filename="1.png")


@app.get("/list_files/")
async def list_files():
    try:
        # 获取 Koharu 文件夹中的文件
        files = os.listdir("Koharu")
        # 过滤掉非文件（如子文件夹）
        files = [f for f in files if os.path.isfile(os.path.join("Koharu", f))]

        # 返回文件列表
        return {"files": files}
    except Exception as e:
        return {"error": str(e)}

if __name__== '__main__':
    uvicorn.run("main:app",reload=True)