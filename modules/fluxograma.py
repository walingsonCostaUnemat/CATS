import streamlit as st
import pandas as pd
from pyvis.network import Network
import tempfile
import streamlit.components.v1 as components

# Função para carregar os dados do CSV
def load_fluxograma_data():
    file_path = 'data/fluxo.csv'
    fluxograma_df = pd.read_csv(file_path)
    return fluxograma_df

# Função para criar o fluxograma interativo
def create_fluxograma_graph(fluxograma_df, selected_etapa=None):
    net = Network(height='750px', width='100%', bgcolor='#222222', font_color='white', directed=True)

    # Adicionar nós e arestas com base nos dados
    if selected_etapa:
        steps = fluxograma_df[selected_etapa].dropna().tolist()
        for i, step in enumerate(steps):
            node_name = f"{selected_etapa}_{i}"
            net.add_node(node_name, label=step, title=step)
            if i > 0:
                net.add_edge(f"{selected_etapa}_{i-1}", node_name)
    else:
        for col in fluxograma_df.columns:
            steps = fluxograma_df[col].dropna().tolist()
            for i, step in enumerate(steps):
                node_name = f"{col}_{i}"
                net.add_node(node_name, label=step, title=step)
                if i > 0:
                    net.add_edge(f"{col}_{i-1}", node_name)

    return net

def show():
    # Carregar os dados do fluxograma
    fluxograma_df = load_fluxograma_data()

    st.title("Fluxograma de Atendimento")
    st.write("Selecione o passo do atendimento:")

    # Adicionar um selectbox para selecionar a coluna/etapa do fluxograma
    etapas = fluxograma_df.columns.tolist()
    etapa_selecionada = st.selectbox("Passo", etapas)

    # Criar o gráfico do fluxograma filtrado
    fluxograma_graph = create_fluxograma_graph(fluxograma_df, etapa_selecionada)

    # Salvar o gráfico como um arquivo HTML temporário
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
        fluxograma_graph.save_graph(tmpfile.name)
        tmpfile.flush()
        with open(tmpfile.name, 'r', encoding='utf-8') as f:
            html_content = f.read()

        components.html(html_content, height=750, width=1000)

    # Exibir as informações correspondentes à etapa selecionada
    st.write(f"### {etapa_selecionada}")
    for descricao in fluxograma_df[etapa_selecionada].dropna():
        st.markdown(f"- {descricao}")

# Chamada para exibir a interface do fluxograma
if __name__ == "__main__":
    show()
