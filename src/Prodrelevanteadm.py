
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import psycopg2

from utils.conect import conectar, fechar_conexao

# Função para conectar ao banco de dados
def executar_consulta(query):
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        fechar_conexao(conn)

# Consulta para obter dados da tabela docente
consulta = "SELECT * FROM prodrelevante where codigoprograma = '32003013014P4';"
dados = executar_consulta(consulta)

# Converter os dados para um DataFrame
df = pd.DataFrame(dados, columns=[
    'Sigla da IES', 'Instituição de Ensino', 'Código do Programa', 'Programa', 'Ano da Publicação',
    'Título', 'Produção Glosada?', 'Ordem', 'Autor', 'Categoria', 'Tipo de Produção', 'Subtipo',
    'Nome do Detalhamento', 'Área de Concentração', 'Linha de Pesquisa',
    'Projeto de Pesquisa', 'A Produção é vinculada a Trabalho de Conclusão?','Valor do Detalhamento'])

# Aplicação Streamlit
st.title('Producao Relevante da Administração ')
st.sidebar.title('Opções')

# Mostrar tabela de dados da primeira consulta
if st.sidebar.checkbox('Mostrar dados da tabela de Produção Relevante'):
    st.dataframe(df)

# Criar 5 gráficos interessantes
st.sidebar.subheader('Análise Gráfica')

# Gráfico de contagem por Ano da Publicação
st.sidebar.markdown('**1. Contagem por Ano da Publicação**')
fig1 = px.histogram(df, x='Ano da Publicação')
st.plotly_chart(fig1)

# Gráfico de contagem por Categoria
st.sidebar.markdown('**2. Contagem por Categoria**')
fig2 = px.bar(df, x='Categoria', title='Contagem por Categoria')
st.plotly_chart(fig2)

# Gráfico de contagem por Tipo de Produção
st.sidebar.markdown('**3. Contagem por Tipo de Produção**')
fig3 = px.bar(df, x='Tipo de Produção', title='Contagem por Tipo de Produção')
st.plotly_chart(fig3)

# Gráfico de contagem por Área de Concentração
st.sidebar.markdown('**4. Contagem por Área de Concentração**')
fig4 = px.bar(df, x='Área de Concentração', title='Contagem por Área de Concentração')
st.plotly_chart(fig4)

# Gráfico de contagem por Linha de Pesquisa
st.sidebar.markdown('**5. Contagem por Linha de Pesquisa**')
fig5 = px.bar(df, x='Linha de Pesquisa', title='Contagem por Linha de Pesquisa')
st.plotly_chart(fig5)

