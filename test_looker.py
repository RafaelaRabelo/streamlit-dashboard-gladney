import streamlit as st
from streamlit_option_menu import option_menu
from urllib.parse import urlencode
import requests
import os
import base64

# Carregar variáveis do .env local (opcional)
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')
ALLOWED_EMAILS_RAW = os.getenv('ALLOWED_EMAILS', '')
ALLOWED_EMAILS = [email.strip() for email in ALLOWED_EMAILS_RAW.split(',') if email.strip()]

AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
TOKEN_URL = 'https://oauth2.googleapis.com/token'
USER_INFO_URL = 'https://www.googleapis.com/oauth2/v2/userinfo'

params = {
    'client_id': CLIENT_ID,
    'response_type': 'code',
    'scope': 'openid email profile',
    'redirect_uri': REDIRECT_URI,
    'access_type': 'offline',
    'prompt': 'consent'
}
auth_request_url = f'{AUTH_URL}?{urlencode(params)}'

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

if not st.session_state['authenticated']:
    st.markdown(f'### 🔐 [Login with Google]({auth_request_url})')

    query_params = st.query_params

    if 'code' in query_params:
        code = query_params['code'][0]

        token_data = {
            'code': code,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'redirect_uri': REDIRECT_URI,
            'grant_type': 'authorization_code'
        }

        token_response = requests.post(TOKEN_URL, data=token_data)
        token_json = token_response.json()

        if 'access_token' in token_json:
            access_token = token_json['access_token']

            user_info_response = requests.get(
                USER_INFO_URL,
                headers={'Authorization': f'Bearer {access_token}'}
            )
            user_info = user_info_response.json()

            user_email = user_info.get('email', '')
            user_name = user_info.get('name', '')

            if ALLOWED_EMAILS:
                permitir_acesso = user_email in ALLOWED_EMAILS
            else:
                permitir_acesso = True  # libera acesso se lista vazia

            if permitir_acesso:
                st.session_state['authenticated'] = True
                st.session_state['user'] = user_info
                st.success(f'✅ Welcome {user_name} ({user_email})')
            else:
                st.error('❌ Email não autorizado para este app.')
                st.stop()
        else:
            st.error('❌ Falha na autenticação.')
            st.stop()

    st.stop()

st.sidebar.success(f"✅ Logged in as {st.session_state['user']['email']}")
st.title('🚀 Dashboard Gladney')
st.write('🔐 Conteúdo protegido liberado!')

# Aqui seu dashboard e conteúdo
