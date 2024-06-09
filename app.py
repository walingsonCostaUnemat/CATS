import streamlit as st
import pandas as pd

# Carregar dados
@st.cache_data
def load_data():
    try:
        glossario_df = pd.read_csv('data/glossario.csv', sep=';')
    except pd.errors.ParserError as e:
        st.error(f"Erro ao ler o arquivo glossario.csv: {e}")
        glossario_df = pd.DataFrame(columns=["Termo", "Definição"])
    
    try:
        rede_apoio_df = pd.read_csv('data/rede_apoio.csv',sep=';')
    except pd.errors.ParserError as e:
        st.error(f"Erro ao ler o arquivo rede_apoio.csv: {e}")
        rede_apoio_df = pd.DataFrame(columns=["Nome", "Contato", "Descrição"])
    
    return glossario_df, rede_apoio_df

glossario_df, rede_apoio_df = load_data()

# Sidebar para navegação
st.sidebar.title("CATS - Curso de Atendimento a Tentativas de Suicídio")
module = st.sidebar.selectbox("Escolha o módulo", ["Página Principal", "Glossário", "Fluxograma", "Rede de Apoio"])

# Carregar o módulo selecionado
if module == "Página Principal":
    from modules import pagina_principal
    pagina_principal.show()
elif module == "Glossário":
    from modules import glossario
    glossario.show(glossario_df)
elif module == "Fluxograma":
    from modules import fluxograma
    fluxograma.show()
elif module == "Rede de Apoio":
    from modules import rede_apoio
    rede_apoio.show(rede_apoio_df)