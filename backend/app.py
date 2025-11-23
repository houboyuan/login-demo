from fastapi import FastAPI, HTTPException, Header, Request
from fastapi.middleware.cors import CORSMiddleware
from auth import AuthService
from typing import Optional
import os

app = FastAPI(title="ByteBase Auth API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

auth_service = AuthService()

@app.get("/")
async def root():
    return {"message": "ByteBase Auth API"}

@app.get("/auth/github")
async def github_login():
    """GitHub登录端点"""
    try:
        url = auth_service.get_github_login_url()
        return {"login_url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/auth/google")
async def google_login():
    """Google登录端点"""
    try:
        url = auth_service.get_google_login_url()
        return {"login_url": url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/auth/github/callback")
async def github_callback(request: Request):
    """GitHub回调处理"""
    try:
        data = await request.json()
        code = data.get("code")
        
        if not code:
            raise HTTPException(status_code=400, detail="Missing code")
        
        # 交换 access token
        access_token = auth_service.exchange_github_code(code)
        if not access_token:
            raise HTTPException(status_code=400, detail="Failed to get access token")
        
        # 获取用户信息
        user_info = auth_service.get_github_user_info(access_token)
        if not user_info:
            raise HTTPException(status_code=400, detail="Failed to get user info")
        
        # 保存到数据库
        auth_service.save_user_to_db(user_info)
        
        return user_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/auth/google/callback")
async def google_callback(request: Request):
    """Google回调处理"""
    try:
        data = await request.json()
        code = data.get("code")
        
        if not code:
            raise HTTPException(status_code=400, detail="Missing code")
        
        # 交换 access token
        access_token = auth_service.exchange_google_code(code)
        if not access_token:
            raise HTTPException(status_code=400, detail="Failed to get access token")
        
        # 获取用户信息
        user_info = auth_service.get_google_user_info(access_token)
        if not user_info:
            raise HTTPException(status_code=400, detail="Failed to get user info")
        
        # 保存到数据库
        auth_service.save_user_to_db(user_info)
        
        return user_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/user/{user_id}")
async def get_user(user_id: str):
    """获取用户信息"""
    user_info = auth_service.get_user_info(user_id)
    if not user_info:
        raise HTTPException(status_code=404, detail="User not found")
    return user_info

@app.get("/users")
async def get_all_users():
    """获取所有用户"""
    users = auth_service.get_all_users()
    return {"users": users}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
