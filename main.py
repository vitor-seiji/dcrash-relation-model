from flask import Flask, jsonify
from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)

# Configurações do Supabase
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

# Criar cliente Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

from routes import *

if __name__ == "__main__":
    app.run(debug=True)