import streamlit as st
import pandas as pd
import plotly.express as px
from utils.conect import conectar, fechar_conexao

 #Função para executar consulta e retornar um cursor
def executar_consulta(query):
    conn, cursor = conectar()
    try:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        return pd.DataFrame(cursor.fetchall(), columns=columns)
    finally:
        fechar_conexao(conn, cursor)


# Atualizar a função fechar_conexao para aceitar o cursor como argumento
def fechar_conexao(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()


## Consulta para obter dados da tabela Pesquisar
consulta_ensino = """SELECT nome, mestradotempocerto, equilibriogenero, pessoalacaddoutorado,
           contatoambientetrabalho, proporcao
    FROM ensinoaprendiz1
    WHERE programa = 'Administracao' OR programa = 'ADMINISTRACAO';"""
df_ensino = executar_consulta(consulta_ensino)

## Consulta para obter dados da tabela Pesquisar
consulta_pesquisar = "SELECT * FROM pesquisar where programa = 'Administracao';"
df_pesquisar = executar_consulta(consulta_pesquisar)

# Consulta para obter dados da tabela Transferência de Conhecimento
consulta_transfconhecimento = "SELECT * FROM transfconhecimento where programa = 'Administracao';"
df_transfconhecimento = executar_consulta(consulta_transfconhecimento)

# Consulta para obter dados da tabela Orientação internacional
consulta_orientacaointern = "SELECT * FROM orientacaointern where programa = 'Administracao';"
df_orientacaointern = executar_consulta(consulta_orientacaointern)

# Consulta para obter dados da tabela engajamento regional
consulta_engajreg = "SELECT * FROM engajreg where programa = 'Administracao';"
df_engajreg = executar_consulta(consulta_engajreg)

# Aplicação Streamlit
st.title('Administração')
st.sidebar.title('Opções')

# Mostrar tabelas de dados
st.sidebar.subheader('Tabelas de Dados')

if st.sidebar.checkbox('Ensino Aprendizagem'):
    # Convertendo a coluna 'proporcao' para float
    df_ensino['proporcao'] = df_ensino['proporcao'].astype(float)

    # Criar o gráfico de dispersão com Plotly Express
    fig = px.scatter(df_ensino, x='mestradotempocerto', y='equilibriogenero', size='proporcao', 
                     hover_name='nome', labels={'mestradotempocerto': 'Mestrado no Tempo Certo', 
                                                'equilibriogenero': 'Equilíbrio de Gênero'})
    
    # Adicionar título
    fig.update_layout(title='Ranking Internacional U-Multirank - Ensino Aprendizagem')
    
    # Exibir o gráfico
    st.plotly_chart(fig)

if st.sidebar.checkbox('Mostrar dados de Pesquisar'):
    st.subheader('Dados de Pesquisar')
    st.dataframe(df_pesquisar.fillna(0))  # Preenchendo os valores nulos com zero

# Tabela de Transferência de Conhecimento
if st.sidebar.checkbox('Mostrar dados de Transferência de Conhecimento'):
    st.subheader('Dados de Transferência de Conhecimento')
    st.dataframe(df_transfconhecimento.fillna(0))  # Preenchendo os valores nulos com zero

# Tabela de Orientação Internacional
if st.sidebar.checkbox('Mostrar dados de Orientação Internacional'):
    st.subheader('Dados de Orientação Internacional')
    st.dataframe(df_orientacaointern.fillna(0))  # Preenchendo os valores nulos com zero

# Tabela de Engajamento Regional
if st.sidebar.checkbox('Mostrar dados de Engajamento Regional'):
    st.subheader('Dados de Engajamento Regional')
    st.dataframe(df_engajreg.fillna(0))  # Preenchendo os valores nulos com zer