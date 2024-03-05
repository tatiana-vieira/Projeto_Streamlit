import streamlit as st
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Desativa o aviso sobre o uso do Pyplot Global
st.set_option('deprecation.showPyplotGlobalUse', False)

# Função para conectar ao banco de dados
from utils.conect import conectar, fechar_conexao

# Atualizar a função fechar_conexao para aceitar o cursor como argumento
def fechar_conexao(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()  

# Função para executar consultas SQL e retornar os resultados como um DataFrame
def executar_consulta(query):
    conn, cursor = conectar()
    if conn:
        try:
            cursor.execute(query)
            df = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
            return df
        except psycopg2.Error as e:
            st.error("Erro ao executar consulta: {}".format(e))
        finally:
            fechar_conexao(conn, cursor)

# Contagem por Título e Tipo de Produção
def contagem_por_titulo():
    query = "select tipoproducao, count(distinct titulo) as quantidade from producaointelectual where codigoprograma = '32003013014P4' group by tipoproducao;"
    return executar_consulta(query)

# Executando a função para obter os dados de títulos
dados_titulos = contagem_por_titulo()
st.write("Tipos de Produção Intelectual:", dados_titulos)

def contagem_subtipos():
    # Função para contar livros por ano de publicação e subtipo
    query = """
        SELECT 
            CAST(anaopublicacao AS INTEGER) AS ano,
            subtipo,
            COUNT(DISTINCT titulo) AS quantidade
        FROM 
            producaointelectual 
        WHERE 
            codigoprograma = '32003013014P4'
        GROUP BY 
            ano, subtipo;
    """
    return executar_consulta(query)  # Suponho que você tenha uma função executar_consulta()

# Executando a função para obter os dados de subtipos
dados_subtipos = contagem_subtipos()

# Mensagem de depuração
st.write("Dados de subtipos de Produção Intelectual:", dados_subtipos)

def prodintelectual_egresso():
    # Consulta SQL para selecionar o nome do egresso e os títulos de produção intelectual associados a ele
 query = """
        SELECT e.nome, p.titulo 
        FROM egresso e
        JOIN producaointelectual p ON e.nome = p.autor
        WHERE e.codigoprograma = '32003013014P4'
        AND p.codigoprograma = '32003013014P4';
    """
 return executar_consulta(query)  # Suponho que você tenha uma função executar_consulta()

    # Executar a consulta SQL e obter os resultados
 df = executar_consulta(query)
    # Verificar se há dados retornados pela consulta

dados_egresso = prodintelectual_egresso()
st.write("Dados de Produção Intelectual de Egressos:", dados_egresso)       

    
   





  