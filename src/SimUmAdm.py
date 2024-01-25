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

# Consulta para obter dados da tabela Ensino Aprendizado
consulta_ensino = "SELECT * FROM ensinoaprendiz1 where programa = 'Administracao' OR programa = 'ADMINISTRACAO';"
dados_ensino = executar_consulta(consulta_ensino)

# Consulta para obter dados da tabela Pesquisar
consulta_pesquisar = "SELECT * FROM pesquisar where programa = 'Administracao';"
dados_pesquisar = executar_consulta(consulta_pesquisar)

# Consulta para obter dados da tabela Transferência de Conhecimento
consulta_transfconhecimento = "SELECT * FROM transfconhecimento where programa = 'Administracao';"
dados_transfconhecimento = executar_consulta(consulta_transfconhecimento)

# Consulta para obter dados da tabela Orientação internacional
consulta_orientacaointern = "SELECT * FROM orientacaointern where programa = 'Administracao';"
dados_orientacaointern = executar_consulta(consulta_orientacaointern)

# Consulta para obter dados da tabela engajamento regional
consulta_engajreg = "SELECT * FROM engajreg where programa = 'Administracao';"
dados_engajreg = executar_consulta(consulta_engajreg)

# Aplicação Streamlit
st.title('Administração')
st.sidebar.title('Opções')

# Mostrar tabelas de dados
st.sidebar.subheader('Tabelas de Dados')


# Tabela de Ensino Aprendizado
if st.sidebar.checkbox('Mostrar dados de Ensino Aprendizado'):
  st.dataframe(pd.DataFrame(dados_ensino, columns=['Mestrado tempo', 'Equilíbrio de Gênero', 'Professores com Doutorado',
                         'Contato Ambiente Trabalho', 'Proporção aluno-professor', 'Mestrado tempo certo(letra)',
                         'Equlibrio Genero(letra)', 'Pessoal Academico Doutorado(letra)', 'Contato Ambiente Trabalho(letra)',
                         'Proporcao(letra)', 'Codigo', 'Nome', 'Sigla', 'País', 'Programa', 'Area Tematica']))
  
    
    
# Tabela de Pesquisar
if st.sidebar.checkbox('Mostrar dados de Pesquisar'):
    st.subheader('Dados de Pesquisar')
    st.dataframe(pd.DataFrame(dados_pesquisar,columns=['Receita Pesq-Externa','Produtividade Doutorado','Numero Publicacao','Taxa Citação','Publ + Citada','Publ Interdiscipl','Publ Acesso Aberto','Orientacao Pesquisa','Porcentagem Autoras','Codigo','Nome','Sigla','País','Programa','Area tematica','Receita Pesquisa Externa(letra)','Produtividade Doutorado(letra)','Publicacao(letra)','Taxa Citação(letra)', 'Publicação Mais Citada(letra)','Publicacao Interd(letra)','Publ.Acesso Aberto(letra)','Orientação Pesquisa(letra)','Autoras(letra)']))

# Tabela de Transferência de Conhecimento
if st.sidebar.checkbox('Mostrar dados de Transferência de Conhecimento'):
    st.subheader('Dados de Transferência de Conhecimento')
    st.dataframe(pd.DataFrame(dados_transfconhecimento))

# Tabela de Orientação Internacional
if st.sidebar.checkbox('Mostrar dados de Orientação Internacional'):
    st.subheader('Dados de Orientação Internacional')
    st.dataframe(pd.DataFrame(dados_orientacaointern))

# Tabela de Engajamento Regional
if st.sidebar.checkbox('Mostrar dados de Engajamento Regional'):
    st.subheader('Dados de Engajamento Regional')
    st.dataframe(pd.DataFrame(dados_engajreg))

# Criar gráficos
st.sidebar.subheader('Análise Gráfica')

# Gráfico de contagem por Categoria para a tabela Pesquisar
if st.sidebar.checkbox('Gráfico: Contagem por Categoria - Pesquisar'):
    st.subheader('Gráfico: Contagem por Categoria - Pesquisar')
    fig_pesquisar = px.bar(pd.DataFrame(dados_pesquisar), x='Categoria', title='Contagem por Categoria')
    st.plotly_chart(fig_pesquisar)

# Adicione mais gráficos conforme necessário para outras tabelas