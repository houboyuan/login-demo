from supabase import create_client, Client
import os
from config import SUPABASE_URL, SUPABASE_KEY

class AuthService:
    def __init__(self):
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    def get_github_login_url(self):
        """获取GitHub登录URL"""
        response = self.supabase.auth.sign_in_with_oauth({
            "provider": "github",
            "options": {
                "redirect_to": f"{os.getenv('REDIRECT_URL')}/callback.html"
            }
        })
        return response.url
    
    def get_google_login_url(self):
        """获取Google登录URL"""
        response = self.supabase.auth.sign_in_with_oauth({
            "provider": "google",
            "options": {
                "redirect_to": f"{os.getenv('REDIRECT_URL')}/callback.html"
            }
        })
        return response.url
    
    def get_user_info(self, access_token):
        """获取用户信息"""
        try:
            # 设置访问令牌
            self.supabase.postgrest.auth(access_token)
            
            # 获取当前用户
            user_response = self.supabase.auth.get_user(access_token)
            if user_response.user:
                user = user_response.user
                return {
                    "id": user.id,
                    "email": user.email,
                    "name": user.user_metadata.get('full_name', ''),
                    "avatar": user.user_metadata.get('avatar_url', ''),
                    "provider": user.app_metadata.get('provider', '')
                }
            return None
        except Exception as e:
            print(f"Error getting user info: {e}")
            return None
    
    def get_all_users(self, access_token):
        """获取所有用户"""
        try:
            self.supabase.postgrest.auth(access_token)
            
            # 从profiles表获取用户信息
            response = self.supabase.table('profiles').select('*').execute()
            return response.data
        except Exception as e:
            print(f"Error getting users: {e}")
            return []
    
    def update_user_profile(self, access_token, user_id, updates):
        """更新用户信息"""
        try:
            self.supabase.postgrest.auth(access_token)
            response = self.supabase.table('profiles').update(updates).eq('id', user_id).execute()
            return response.data
        except Exception as e:
            print(f"Error updating user: {e}")
            return None
