import streamlit as st
from components import admin_header
from utils import librion_api

# 1. Configuração da página
st.set_page_config(page_title="Admin - Unidades", layout="wide")

# Verificação de segurança: Apenas administradores
def check_login():
    user = st.session_state.get("user")
    is_admin = st.session_state.get("is_admin")

    if not user or not is_admin:
        st.error("Acesso restrito a administradores.")
        st.button("Login", type='primary')
        st.stop()

# Recebe todas as bibliotecas cadastradas
def fetch_registered_libraries():
    response = librion_api("GET", "/libraries/")

    if response.get("success"):
        st.session_state.registered_libraries = response["data"]
        return response["data"]
    
    else:
        st.info("Nenhuma Biblioteca Cadastrada!")

# Registra um novo usuário
def register_library(name, email, password, cep):
    json = {
        "name": name,
        "email": email,
        "password": password,
        "cep": cep
    }

    response = librion_api("POST", "/auth/library", json=json)

    if response.get("success"):
        st.toast("Nova biblioteca adicionada!")
        st.balloons()
    
    else:
        st.toast(f"Erro:{response["error"]["detail"]}")

# Renderiza formulário de biblioteca
def render_form_register():
    with st.form("form_biblioteca", clear_on_submit=True):
        st.subheader("Dados da Biblioteca")
    
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Nome da Unidade")
            email = st.text_input("E-mail")
        
        with col2:
            password = st.text_input("Senha", type="password")
            cep = st.text_input("CEP")

        st.write("##")
        enviar = st.form_submit_button("Cadastrar Unidade", type="primary")

        if enviar:
            if name.strip() and email.strip() and password.strip():
                register_library(name, email, password, cep)
                fetch_registered_libraries()
            else:
                st.error("Campos nome, senha e cep são obrigatórios")

# Renderiza todas as bibliotecas
def render_list_libraries():
    st.subheader("Rede de Bibliotecas")
    unidades = fetch_registered_libraries()
    st.dataframe(unidades, use_container_width=True, hide_index=True)

# Render page
def render_page():
    check_login()
    admin_header()

    st.title("🏢 Gestão de Unidades")
    st.write("Gerencie as bibliotecas físicas que compõem a rede municipal.")
    
    
    tab_cadastro, tab_lista = st.tabs(["➕ Nova Unidade", "📋 Unidades Ativas"])

    # --- ABA 1: FORMULÁRIO DE CADASTRO ---
    with tab_cadastro:
        render_form_register()

    # --- ABA 2: LISTAGEM ---
    with tab_lista:
        render_list_libraries()

render_page()