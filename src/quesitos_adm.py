import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import psycopg2
import seaborn as sns

# Desativa o aviso sobre o uso do Pyplot Global
st.set_option('deprecation.showPyplotGlobalUse', False)

from utils.conect import conectar, fechar_conexao

# Função para conectar ao banco de dados
def executar_consulta(query):
    conn, cursor = conectar()
    try:
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        fechar_conexao(conn, cursor)

# Atualizar a função fechar_conexao para aceitar o cursor como argumento
def fechar_conexao(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()
# Função para consultar discentes no banco de dados
consulta_quesitos = "select * from avaliacaoprog_adm"

dados_quesitos = executar_consulta(consulta_quesitos)

# Converter os resultados da consulta para um DataFrame do pandas
df_quesitos = pd.DataFrame(dados_quesitos, columns=['Quesitos', '2017', '2021'])
