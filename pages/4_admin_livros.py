import streamlit as st
from components import admin_header
from utils import librion_api
import time

st.set_page_config(page_title="Admin - Cadastrar Livro", layout="wide")

#verificação de login
def check_login():
    user = st.session_state.get("user")
    is_admin = st.session_state.get("is_admin")

    if not user or not is_admin:
        st.error("Acesso negado! Esta página é restrita a administradores.")
        st.button("Voltar para Home", on_click=lambda: st.switch_page("Home.py"))
        st.stop()

#Busca todos os livros e salva no state
def fetch_books():
    response = librion_api("GET", "/libraries/me/copies", token=st.session_state.auth_token)

    if response["success"]:
        st.session_state.library_books = response["data"]
    
    else:
        st.toast(f"Erro ao requisitar os livros:{response["error"]['detail']}")

#registra um novo livro
def register_book(isbn, quantity, is_global=True):
    body = {
        "isbn": isbn,
        "quantity": quantity,
        "is_global": is_global
    }

    response = librion_api(
        "POST",
        "/libraries/me/copies",
        json=body,
        token=st.session_state.auth_token
    )

    if response["success"]:
        st.toast("Livro cadastrado com sucesso!")
        fetch_books()
    else:
        st.toast(f"Erro no cadastro: {response['error']['detail']}")

#excluir livro
def delete_book(copy_id):
    response = librion_api(
        "DELETE",
        f"/libraries/me/copies/{copy_id}",
        token=st.session_state.auth_token
    )

    if response["success"]:
        st.toast("Livro removido com sucesso!")
        st.rerun()
    else:
        st.error(f"Erro ao excluir: {response['error']}")

#formulario cadastro livro
def render_book_form():
    with st.container(border=True, width='stretch'):
        col1, col2 = st.columns([3, 1])

        with col1:
            isbn = st.text_input("ISBN")

        with col2:
            quantity = st.number_input(
                "Quantidade de Exemplares",
                min_value=1,
                step=1
            )

            is_global = st.toggle("Global?")

    if st.button("Cadastrar Livro", type="primary"):
        if not isbn:
            st.warning("Informe o ISBN")
            return

        register_book(isbn, quantity, is_global)

#lista de livros (sem grid)+botao excluir
def render_book_list():
    st.divider()
    st.subheader("📚 Livros Cadastrados")
    
    fetch_books()
    books = st.session_state.get("library_books")

    if not books:
        st.info("Nenhum livro cadastrado ainda.")
        return

    for item in books:
        book = item.get("book", {})

        with st.container(border=True):
            col1, col2, col3 = st.columns([1, 3, 1])
            url_image = book.get("image")

            #imagem do livro
            with col1:
                if url_image and not url_image == "(vazio)":
                    st.image(url_image, width=150)
        
                else:
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

            #informações do livro
            with col2:
                st.markdown(f"### {book['title']}")
                st.write(f"**Autor:** {book['author']}")
                st.write(f"**ISBN:** {book['isbn']}")

                st.write(
                    f"**Disponíveis:** {item['quantity_available']} "
                    f"de {item['quantity']}"
                )

                with st.expander("Descrição"):
                    st.write(book["description"])

            #botao excluir
            with col3:
                st.write("")  
                st.write("")

                if st.button("🗑 Excluir", key=f"del_{item['id']}"):
                    delete_book(item["id"])

#pag principal
def render_page():
    
    check_login()
    admin_header()
    
    st.subheader("📑 Gestão de Acervo")
    st.caption("Cadastrar Novo Livro")

    render_book_form()
    render_book_list()

render_page()