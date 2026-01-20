import streamlit as st
from components import visitor_header
from utils import librion_api
import time

# Configuração da página para esconder a barra lateral e focar no login
st.set_page_config(page_title="Librion | Login", layout="wide", initial_sidebar_state="collapsed")

# Busca o acess_token da api
def get_token(email, password, is_admin = False):
    credentials = {
        "email": email, 
        "password": password, 
        "admin": is_admin
    }

    response = librion_api("POST", "/auth/login", json=credentials)
    return response.get("data", {}).get("access_token")

# Busca os dados do usuário por o token
def get_user(token, is_admin = False):
    request_route = "/libraries/me" if is_admin else "/readers/me"
    response = librion_api("GET", request_route, token=token)
    
    return response.get("data")

# Redireciona para a página de usuário ou admnistrador
def redirect_page(is_admin):
    page = "pages/4_admin_livros.py" if is_admin else "pages/7_minha_conta.py" 
    st.switch_page(page)

# Validar Login
def validate_login(email, password, is_admin = False):
    # Email ou senha vazios
    if not email.strip() or not password.strip():
        st.error("Preencha todos os campos!")
    
    else:
        # Busca o token e após isso o usuário
        with st.spinner("Autenticando..."):
            time.sleep(1)
            token = get_token(email, password, is_admin)
            user = get_user(token, is_admin) if token else None

        # Se existir um usuário
        if user:
            st.session_state.user = user
            st.session_state.auth_token = token
            st.session_state.is_admin = is_admin

            #Redireciona para a página (depende se é admin ou não)
            redirect_page(is_admin)
        
        else:
            st.error("Usuário ou senha errados! Tente novamente")
            st.stop()

# Card da lateral esquerda
def card_banner():
    with st.container(border=True): # Simula o card azul da imagem
        st.image("https://images.unsplash.com/photo-1507842217343-583bb7270b66?q=80&w=1000", caption="Bem-vindo ao Librion")
        st.markdown("### Faça parte da rede integrada de bibliotecas municipais de Crato-CE")

# Cada da lateral direita
def card_login():
    st.subheader("Acesse sua conta")
    st.write("Entre com suas credenciais para acessar o Librion")
    
    email = st.text_input("E-mail", placeholder="seu@email.com")
    password = st.text_input("Senha", type="password", placeholder="********")
    
    btn_login = st.button("Fazer Login", type="primary", width='stretch')
    btn_is_admin = st.toggle("Admin", True)

    if btn_login:
        validate_login(email, password, btn_is_admin)

# Renderiza a página        
def render_login_page():
    visitor_header()

    _, center, _ = st.columns([1, 4, 1])

    with center:
        col_img, col_form = st.columns([1, 1], gap="large")

        with col_img:
            card_banner()

        with col_form:
            card_login()

render_login_page()