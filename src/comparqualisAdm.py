import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
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

# Consulta para obter dados da tabela docente
consulta_capes1 = """
SELECT sigla, quadrienal, nota FROM resultadoavaliacao where area_avaliacao = 'ADMINISTRAÇÃO PÚBLICA E DE EMPRESAS, CIÊNCIAS CONTÁBEIS E TURISMO'
and nota ='3'"""
dados_capes1 = executar_consulta(consulta_capes1)

consulta_capes2 = """
SELECT sigla, quadrienal, nota FROM resultadoavaliacao where area_avaliacao = 'ADMINISTRAÇÃO PÚBLICA E DE EMPRESAS, CIÊNCIAS CONTÁBEIS E TURISMO'
and nota ='4'"""
dados_capes2 = executar_consulta(consulta_capes2)

consulta_capes3 = """
SELECT sigla, quadrienal, nota FROM resultadoavaliacao where area_avaliacao = 'ADMINISTRAÇÃO PÚBLICA E DE EMPRESAS, CIÊNCIAS CONTÁBEIS E TURISMO'
and nota ='5' or nota ='6'"""
dados_capes3 = executar_consulta(consulta_capes3)

# Colocar os dados em DataFrames do pandas
df_capes1 = pd.DataFrame(dados_capes1, columns=['Sigla', 'Quadrienal', 'Nota'])
df_capes2 = pd.DataFrame(dados_capes2, columns=['Sigla', 'Quadrienal', 'Nota'])
df_capes3 = pd.DataFrame(dados_capes3, columns=['Sigla', 'Quadrienal', 'Nota'])

# Mostrar os diagramas de barras
st.subheader("Nota 3")
st.bar_chart(df_capes1.set_index('Sigla')['Quadrienal'])

st.subheader("Nota 4")
st.bar_chart(df_capes2.set_index('Sigla')['Quadrienal'])

st.subheader("Nota 5 ou 6")
st.bar_chart(df_capes3.set_index('Sigla')['Quadrienal'])