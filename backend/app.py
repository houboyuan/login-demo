from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from auth_simple import SimpleAuthService
from typing import Optional
import os

app = FastAPI(title="ByteBase Auth API")

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

auth_service = SimpleAuthService()

@app.get("/")
async def root():
    return {"message": "ByteBase Auth API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

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

@app.get("/user")
async def get_current_user(authorization: Optional[str] = Header(None)):
    """获取当前用户信息"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")
    
    access_token = authorization.replace("Bearer ", "")
    user_info = auth_service.get_user_info(access_token)
    
    if not user_info:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return user_info

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
