import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
REDIRECT_URL = os.getenv("REDIRECT_URL", "https://houboyuan.github.io/login-demo")

import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://xnhbznmrgzlzrhjninhv.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhuaGJ6bm1yZ3psenJoam5pbmh2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM4ODMyODksImV4cCI6MjA3OTQ1OTI4OX0.PtGOG40-QMVTb8NE2OEvbap6wOwi6YS6-ZKWypSfno0")
REDIRECT_URL = os.getenv("REDIRECT_URL", "https://houboyuan.github.io/login-demo")
