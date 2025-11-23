from supabase import create_client, Client
import os
from config import SUPABASE_URL, SUPABASE_KEY
import requests
import json

class AuthService:
    def __init__(self):
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    def get_github_login_url(self):
        """手动构建 GitHub OAuth URL"""
        client_id = os.getenv("GITHUB_CLIENT_ID")
        redirect_uri = f"{os.getenv('REDIRECT_URL')}/callback.html"
        scope = "user:email"
        return f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}"
    
    def get_google_login_url(self):
        """手动构建 Google OAuth URL"""
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        redirect_uri = f"{os.getenv('REDIRECT_URL')}/callback.html"
        scope = "https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email"
        return f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&response_type=code"
    
    def exchange_github_code(self, code):
        """使用 GitHub code 交换 access token"""
        client_id = os.getenv("GITHUB_CLIENT_ID")
        client_secret = os.getenv("GITHUB_CLIENT_SECRET")
        
        response = requests.post(
            "https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "code": code,
                "redirect_uri": f"{os.getenv('REDIRECT_URL')}/callback.html"
            }
        )
        
        if response.status_code == 200:
            return response.json().get("access_token")
        return None
    
    def exchange_google_code(self, code):
        """使用 Google code 交换 access token"""
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        
        response = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "client_id": client_id,
                "client_secret": client_secret,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": f"{os.getenv('REDIRECT_URL')}/callback.html"
            }
        )
        
        if response.status_code == 200:
            return response.json().get("access_token")
        return None
    
    def get_github_user_info(self, access_token):
        """获取 GitHub 用户信息"""
        response = requests.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        if response.status_code == 200:
            user_data = response.json()
            return {
                "id": user_data["id"],
                "email": user_data.get("email", ""),
                "name": user_data.get("name", user_data.get("login", "")),
                "avatar": user_data.get("avatar_url", ""),
                "provider": "github"
            }
        return None
    
    def get_google_user_info(self, access_token):
        """获取 Google 用户信息"""
        response = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        
        if response.status_code == 200:
            user_data = response.json()
            return {
                "id": user_data["id"],
                "email": user_data.get("email", ""),
                "name": user_data.get("name", ""),
                "avatar": user_data.get("picture", ""),
                "provider": "google"
            }
        return None
    
    def save_user_to_db(self, user_info):
        """保存用户信息到 Supabase 数据库"""
        try:
            response = self.supabase.table("profiles").upsert({
                "id": str(user_info["id"]),
                "email": user_info["email"],
                "full_name": user_info["name"],
                "avatar_url": user_info["avatar"],
                "provider": user_info["provider"]
            }).execute()
            return response.data
        except Exception as e:
            print(f"Error saving user to DB: {e}")
            return None
    
    def get_user_info(self, user_id):
        """从数据库获取用户信息"""
        try:
            response = self.supabase.table("profiles").select("*").eq("id", user_id).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error getting user from DB: {e}")
            return None
    
    def get_all_users(self):
        """获取所有用户"""
        try:
            response = self.supabase.table("profiles").select("*").execute()
            return response.data
        except Exception as e:
            print(f"Error getting users: {e}")
            return []
