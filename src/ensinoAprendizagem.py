import streamlit as st
import pandas as pd
import plotly.express as px
import psycopg2

from utils.conect import conectar, fechar_conexao

# Função para executar consulta e retornar um cursor
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

# Consulta para obter dados da tabela Ensino Aprendizado
consulta_ensino = "SELECT * FROM ensinoaprendiz1 where programa = 'Administracao' OR programa = 'ADMINISTRACAO';"
cursor_ensino = executar_consulta(consulta_ensino)

st.dataframe(cursor_ensino.fillna(0))  # Preenchendo os valores nulos com zero



