import streamlit as st
import pandas as pd

# Exemplo de dados
dados_objetivos = {
    'ID': [1, 2, 3],
    'Objetivo': ['Objetivo 1', 'Objetivo 2', 'Objetivo 3']
}

dados_metas = {
    'ID': [1, 2, 3, 4, 5],
    'Objetivo_ID': [1, 1, 2, 2, 3],
    'Meta': ['Meta 1', 'Meta 2', 'Meta 3', 'Meta 4', 'Meta 5']
}

# Criar DataFrames com os dados
df_objetivos = pd.DataFrame(dados_objetivos)
df_metas = pd.DataFrame(dados_metas)

# Mostrar os objetivos e metas em uma tabela
st.write("### Objetivos e Metas")

# Loop pelos objetivos
for index, objetivo in df_objetivos.iterrows():
    st.write(f"**{objetivo['Objetivo']}**")
    
    # Filtrar metas relacionadas a este objetivo
    metas_relacionadas = df_metas[df_metas['Objetivo_ID'] == objetivo['ID']]
    
    # Exibir metas e espaço para ações
    for _, meta in metas_relacionadas.iterrows():
        st.write(f"- {meta['Meta']}")
        # Espaço para ações e progresso
        acoes = st.text_area("Ações para esta meta:")
        progresso = st.slider("Progresso realizado (%)", 0, 100, 0)
        st.write("---")