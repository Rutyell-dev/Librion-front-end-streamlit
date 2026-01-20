import streamlit as st
from components import user_header
from datetime import datetime
from utils import librion_api

# 1. Configuração da página
st.set_page_config(page_title="Librion - Minha Conta", layout="wide")

# Busca os empréstimos na API
def fetch_loans():
    response = librion_api("GET", "/readers/me/loans", token=st.session_state.get("auth_token"))
    st.session_state.loans = response.get("data")

    return st.session_state.loans

# Verifica se o usuário está logado
def check_login():
    user = st.session_state.get("user")

    if not user:
        st.error("Por favor, faça login para acessar esta página.")
        st.button("Ir para Login", on_click=lambda: st.switch_page("pages/2_Login.py"))
        st.stop()

# Renderiza o perfil
def render_profile():
    response = librion_api("GET", "/readers/me", token=st.session_state.get("auth_token"))

    if response["success"]:
        profile = response["data"]
        name = profile["name"]
        library = profile["library"]["name"]

        col_av, col_info = st.columns([1, 8])
        
        # Logo com o nome
        with col_av:
            st.markdown(
                f"""<div 
                    style='background-color:#456e7d; 
                    color:white; border-radius:50%; 
                    width:80px; 
                    height:80px; 
                    display:flex; 
                    align-items:center; 
                    justify-content:center; 
                    font-size:30px;'>{name[0:2]}
                </div>""", unsafe_allow_html=True)

        # Nome do usuário
        with col_info:
            st.subheader(name)
            st.caption(f"📍 Biblioteca de Referência: {library}")

        st.write("##")

# Renderiza os cartões de métricas
def render_metrics_cards(total_loans, total_books, next_return_date):
    # --- CARDS DE MÉTRICAS ---
    m1, m2, m3 = st.columns(3)
    with m1:
        with st.container(border=True):
            st.write("📖 **Empréstimos Ativos**")
            st.title("2")
            st.progress(2/5, text="2 de 5 permitidos")

    with m2:
        with st.container(border=True):
            st.write("⭐ **Livros Lidos**")
            st.title("28")
            st.caption("neste ano")

    with m3:
        with st.container(border=True):
            st.write("⏰ **Prazo Próximo**")
            st.title("5")
            st.caption("dias para devolução")

    st.write("##")

# Converte datas da API para o formato dd/mm/yyyy
def iso_to_ddmmyyyy(data_iso: str) -> str:
    data = datetime.fromisoformat(data_iso.replace("Z", "+00:00"))
    return data.strftime("%d/%m/%Y")

# Renderiza um empréstimo
def render_book_loan(loan:dict):
    with st.container(border=True):
        
        copy = loan.get("copy_data", {})
        library = copy.get("library", {})
        book = copy.get("book", {})
        image = book.get("image")

        request_date = iso_to_ddmmyyyy(loan["request_date"])
        return_date = iso_to_ddmmyyyy(loan["return_date"])
        
        c1, c2, c3 = st.columns([1, 4, 2])

        with c1:
            if not image or image == "(vazio)":
                st.markdown(
                    """
                        <div style="
                            width: 100%;
                            height: 250px;
                            background-color: #e0e0e0;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            color: black;
                            border-radius: 8px;
                        ">
                            Sem capa
                        </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.image(image, width=150)


        with c2:
            st.markdown(f"**{book["title"]}**")
            st.caption(f"{book["author"]}")
            st.caption(f"Biblioteca: {library["name"]}")
            if loan["active"]:
                st.warning("Pendente") 
            else: 
                st.success("Concluído")
        
        with c3:
            st.write(f"📅 Empréstimo: {request_date} | Devolução: {return_date}")

# Renderiza todos os empréstimos
def render_loans(loans):
    st.markdown("### Histórico de Empréstimos")

    for loan in loans:
        render_book_loan(loan)

def render_page():
    # Verifica se está logado
    check_login()
    
    # Header
    user_header()

    # Renderiza o perfil
    render_profile()

    st.divider()

    # Busca os emprëstimos
    loans = fetch_loans()

    # Se existir, renderiza
    if loans:
        render_loans(loans)

render_page()