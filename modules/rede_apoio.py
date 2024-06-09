import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import re

def extract_coordinates(link):
    # Extrair coordenadas da URL do Google Maps
    match = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', link)
    if match:
        return float(match.group(1)), float(match.group(2))
    return None, None

def show(rede_apoio_df):
    st.title("Rede de Apoio")
    st.write("Contatos e informações úteis:")

    # Verificar se as colunas necessárias estão presentes
    required_columns = ["CIDADE", "REFERÊNCIA", "TELEFONE", "ENDEREÇO"]
    if not all(column in rede_apoio_df.columns for column in required_columns):
        st.error(f"O arquivo rede_apoio.csv deve conter as colunas: {', '.join(required_columns)}")
        return

    if rede_apoio_df.empty:
        st.write("Nenhuma informação encontrada na rede de apoio.")
        return

    # Campo de busca de cidades com autocomplete
    cidades = sorted(rede_apoio_df['CIDADE'].unique())
    cidade_selecionada = st.selectbox("Buscar cidade:", [""] + cidades)

    # Configurar mapa interativo com uma camada de azulejo para detalhes
    m = folium.Map(location=[-15.77972, -47.92972], zoom_start=5)  # Centro inicial do mapa no Brasil
    folium.TileLayer('OpenStreetMap').add_to(m)

    if cidade_selecionada:
        df_filtrado = rede_apoio_df[rede_apoio_df['CIDADE'] == cidade_selecionada]
    else:
        df_filtrado = rede_apoio_df

    latitudes = []
    longitudes = []

    for index, row in df_filtrado.iterrows():
        link = row['ENDEREÇO']
        if not link.startswith("http://") and not link.startswith("https://"):
            link = "http://" + link

        lat, lon = extract_coordinates(link)
        if lat is not None and lon is not None:
            latitudes.append(lat)
            longitudes.append(lon)
            popup_text = f"{row['REFERÊNCIA']}<br>Telefone: {row['TELEFONE']}<br>Endereço: {row['ENDEREÇO']}"
            folium.Marker([lat, lon], tooltip=row['REFERÊNCIA'], popup=popup_text).add_to(m)
    
    if latitudes and longitudes:
        # Ajustar o mapa para centralizar e aproximar na área dos marcadores
        m.fit_bounds([[min(latitudes), min(longitudes)], [max(latitudes), max(longitudes)]])
    else:
        # Fallback para localização inicial se nenhuma coordenada válida for encontrada
        m.location = [-15.77972, -47.92972]
        m.zoom_start = 5

    # Exibir mapa interativo
    st_folium(m, width=700, height=500)

    # Exibir informações da rede de apoio abaixo do mapa
    st.write("## Lista de Referências")
    if df_filtrado.empty:
        st.write(f"Nenhuma informação encontrada para a cidade {cidade_selecionada}.")
    else:
        for index, row in df_filtrado.iterrows():
            st.markdown(f"**{row['REFERÊNCIA']}** em {row['CIDADE']}")
            st.markdown(f"Telefone: {row['TELEFONE']}")
            st.markdown(f"Endereço: [🔗]({row['ENDEREÇO']})", unsafe_allow_html=True)
            st.markdown("---")

# Adicionar o código CSS para os ícones do Font Awesome
st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
""", unsafe_allow_html=True)
