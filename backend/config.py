import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# 重定向URL - 替换为你的GitHub Pages URL
REDIRECT_URL = "https://yourusername.github.io/bytebase-login"