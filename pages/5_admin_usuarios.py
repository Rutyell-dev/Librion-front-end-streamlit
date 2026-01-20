import streamlit as st
from components import admin_header
from utils import librion_api

#configuracao da pagina
st.set_page_config(page_title="Admin - Usuários", layout="wide")

#verificação de login
def check_login():
    user = st.session_state.get("user")
    is_admin = st.session_state.get("is_admin")

    if not user or not is_admin:
        st.error("Acesso negado! Esta página é restrita a administradores.")
        st.button("Voltar para Home", on_click=lambda: st.switch_page("Home.py"))
        st.stop()

# Busca os leitores cadastrados no banco de dados
def fetch_readers():
    response = librion_api("GET", "/libraries/me/readers", token=st.session_state.get("auth_token"))
    
    if response.get("success"):
        st.session_state.library_readers = response["data"]
        return response["data"]
    
    else:
        st.info("Nenhum leitor cadastrado na biblioteca")
        st.stop()

#POST Reader
def create_reader(name, email, cep, password):
    json = {
        "name": name,
        "email": email,
        "cep": cep,
        "password": password
    }

    token = st.session_state.get("auth_token")
    response = librion_api("POST", "/libraries/me/readers", json=json, token=token)

    if response["success"]:
        st.toast("Usuário cadastrado!")
        st.balloons()
    else:
        st.toast(f"Erro no cadastro: {response['error']['detail']}")

#renderiza o formulário do escritor
def render_reader_form():
    with st.container(border=True):
        st.subheader("Informações do Novo Usuário")

        col1, col2 = st.columns(2)

        with col1:
            nome = st.text_input("Nome Completo")
            email = st.text_input("E-mail")

        with col2:
            cep = st.text_input("CEP")
            senha = st.text_input("Senha", type="password")

        if st.button("Criar Conta", type="primary", use_container_width=True):

            if not nome.strip() or not email.strip() or not cep.strip() or not senha.strip():
                st.warning("Preencha todos os campos!")
            else:
                create_reader(nome, email, cep, senha)

# Renderiza os usuário cadastros
def render_list_readers():
    st.subheader("Usuários Cadastrados")
    readers = fetch_readers()

    #lista visual bonita
    for u in readers:
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"### {u['name']}")
                st.write(f"📧 **Email:** {u['email']}")
                st.write(f"📍 **CEP:** {u['cep']}")

            with col2:
                st.write("")
                st.write("")
                st.button("🗑 Excluir", key=u["email"])

def render_page():
    check_login()
    
    admin_header()

    st.title("👥 Gestão de Usuários")
    tab1, tab2 = st.tabs(["🆕 Cadastrar Novo", "📋 Lista de Usuários"])
    
    with tab1:
        render_reader_form()
    
    with tab2:
        render_list_readers()

render_page()