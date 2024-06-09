import streamlit as st
from streamlit_option_menu import option_menu

# Função para carregar favoritos salvos
def load_favorites():
    return st.session_state.get('favorites', [])

# Função para salvar favoritos
def save_favorite(term):
    if 'favorites' not in st.session_state:
        st.session_state['favorites'] = []
    st.session_state['favorites'].append(term)

# Função para carregar anotações
def load_notes():
    return st.session_state.get('notes', {})

# Função para salvar anotações
def save_note(term, note):
    if 'notes' not in st.session_state:
        st.session_state['notes'] = {}
    st.session_state['notes'][term] = note

def show(glossario_df):
    st.title("Glossário CATS")
    st.write("Termos e definições importantes:")

    # Carregar favoritos e notas
    favorites = load_favorites()
    notes = load_notes()

    # Ordenar o glossário em ordem alfabética
    glossario_df = glossario_df.sort_values(by="Termo")

    # Barra de busca
    search_term = st.text_input("Buscar termo:")

    if not search_term:
        filtered_glossario = glossario_df
    else:
        filtered_glossario = glossario_df[glossario_df["Termo"].str.contains(search_term, case=False, na=False)]

    if filtered_glossario.empty:
        st.write("Nenhum termo encontrado.")
    else:
        for index, row in filtered_glossario.iterrows():
            term = row['Termo']
            with st.expander(f"**{term}**"):
                st.write(row["Definição"])

                # Ícones de opções
                col1, col2 = st.columns([1, 9])
                with col1:
                    option_selected = st.button('⋮', key=f"options_{term}")
                with col2:
                    st.write("")

                if option_selected:
                    # Botão de favorito
                    if st.button(f"Favoritar {term}", key=f"fav_{term}"):
                        save_favorite(term)
                        st.success(f"'{term}' adicionado aos favoritos.")

                    # Área de texto para anotações
                    note = notes.get(term, "")
                    new_note = st.text_area(f"Anotações sobre {term}:", value=note, key=f"note_{term}")
                    if st.button(f"Salvar Anotações {term}", key=f"save_note_{term}"):
                        save_note(term, new_note)
                        st.success(f"Anotações sobre '{term}' salvas.")

    # Exibir termos favoritos
    if favorites:
        st.sidebar.subheader("Termos Favoritos")
        for term in favorites:
            st.sidebar.markdown(f"- {term}")
