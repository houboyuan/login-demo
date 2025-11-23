import os
import requests
from config import SUPABASE_URL, SUPABASE_KEY

class SimpleAuthService:
    def __init__(self):
        self.supabase_url = SUPABASE_URL
        self.supabase_key = SUPABASE_KEY
    
    def get_github_login_url(self):
        """获取GitHub登录URL"""
        try:
            redirect_uri = f"{os.getenv('REDIRECT_URL', 'https://houboyuan.github.io/login-demo')}/callback.html"
            # 直接构建 Supabase OAuth URL
            login_url = f"{self.supabase_url}/auth/v1/authorize"
            params = {
                "provider": "github",
                "redirect_to": redirect_uri
            }
            return f"{login_url}?provider=github&redirect_to={redirect_uri}"
        except Exception as e:
            print(f"Error creating GitHub login URL: {e}")
            # 备用方案
            return f"{self.supabase_url}/auth/v1/authorize?provider=github"
    
    def get_google_login_url(self):
        """获取Google登录URL"""
        try:
            redirect_uri = f"{os.getenv('REDIRECT_URL', 'https://houboyuan.github.io/login-demo')}/callback.html"
            return f"{self.supabase_url}/auth/v1/authorize?provider=google&redirect_to={redirect_uri}"
        except Exception as e:
            print(f"Error creating Google login URL: {e}")
            return f"{self.supabase_url}/auth/v1/authorize?provider=google"
    
    def get_user_info(self, access_token):
        """获取用户信息"""
        try:
            headers = {
                "Authorization": f"Bearer {access_token}",
                "apikey": self.supabase_key
            }
            
            response = requests.get(
                f"{self.supabase_url}/auth/v1/user", 
                headers=headers
            )
            
            if response.status_code == 200:
                user_data = response.json()
                return {
                    "id": user_data.get("id"),
                    "email": user_data.get("email"),
                    "name": user_data.get("user_metadata", {}).get("full_name", ""),
                    "avatar": user_data.get("user_metadata", {}).get("avatar_url", ""),
                    "provider": user_data.get("app_metadata", {}).get("provider", "")
                }
            else:
                print(f"Error fetching user: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Error getting user info: {e}")
            return None
