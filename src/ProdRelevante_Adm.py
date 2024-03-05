import streamlit as st
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Desativa o aviso sobre o uso do Pyplot Global
st.set_option('deprecation.showPyplotGlobalUse', False)


# Função para conectar ao banco de dados
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

# Contagem por Ano da Publicação
def contagem_por_ano():
    query = """SELECT ano, COUNT(DISTINCT titulo) AS count 
            FROM prodrelevante 
            WHERE codigoprograma = '32003013014P4' 
            GROUP BY ano 
            ORDER BY ano;"""
    df = executar_consulta(query)
    if df is not None:
        plt.figure(figsize=(10, 6))
        sns.barplot(data=df, x='ano', y='count')
        plt.xlabel('Ano da Publicação')
        plt.ylabel('Contagem')
        plt.title('Contagem por Ano da Publicação')
        st.pyplot()

# Contagem por Categoria
def contagem_por_categoria():
    query = "SELECT categoria, COUNT(DISTINCT titulo) AS count FROM prodrelevante WHERE codigoprograma = '32003013014P4' GROUP BY categoria"
    df = executar_consulta(query)
    if df is not None:
        plt.figure(figsize=(10, 6))
        sns.barplot(data=df, x='categoria', y='count')
        plt.xlabel('Categoria')
        plt.ylabel('Contagem')
        plt.title('Contagem por Categoria')
        plt.xticks(rotation=45, ha='right')
        st.pyplot()

# Contagem por Tipo de Produção
def contagem_por_tipo_producao():
    query = """SELECT tipoproducao, COUNT(DISTINCT titulo) AS count 
        FROM prodrelevante 
        WHERE codigoprograma = '32003013014P4' 
        GROUP BY tipoproducao;"""
    df = executar_consulta(query)
    if df is not None:
        plt.figure(figsize=(10, 6))
        sns.barplot(data=df, x='tipoproducao', y='count')
        plt.xlabel('Tipo de Produção')
        plt.ylabel('Contagem')
        plt.title('Contagem por Tipo de Produção')
        plt.xticks(rotation=45, ha='right')
        st.pyplot()

# Contagem por Área de Concentração
def contagem_por_area_concentracao():
    query = "SELECT areaconcentracao, COUNT(DISTINCT titulo) AS count FROM prodrelevante WHERE codigoprograma = '32003013014P4'GROUP BY areaconcentracao"
    df = executar_consulta(query)
    if df is not None:
        plt.figure(figsize=(10, 6))
        sns.barplot(data=df, x='areaconcentracao', y='count')
        plt.xlabel('Área de Concentração')
        plt.ylabel('Contagem')
        plt.title('Contagem por Área de Concentração')
        plt.xticks(rotation=45, ha='right')
        st.pyplot()

# Contagem por Linha de Pesquisa
def contagem_por_linha_pesquisa():
    query = "SELECT linhapesquisa, COUNT(DISTINCT titulo) AS count FROM prodrelevante WHERE codigoprograma = '32003013014P4'GROUP BY linhapesquisa"
    df = executar_consulta(query)
    if df is not None:
        plt.figure(figsize=(10, 6))
        sns.barplot(data=df, x='linhapesquisa', y='count')
        plt.xlabel('Linha de Pesquisa')
        plt.ylabel('Contagem')
        plt.title('Contagem por Linha de Pesquisa')
        plt.xticks(rotation=45, ha='right')
        st.pyplot()

# Mostrar os autores de cada título
def mostrar_autores_por_titulo():
    query = "SELECT titulo, autor,categoria FROM prodrelevante where autor != ''"
    df = executar_consulta(query)
    if df is not None:
        st.write(df)

def mostrarprod_egresso():
    query="""SELECT e.nome, p.titulo 
    FROM egresso e
    JOIN prodrelevante p ON e.nome = p.autor
    WHERE e.codigoprograma = '32003013014P4'
    AND p.codigoprograma = '32003013014P4'"""
    
    df = executar_consulta(query)
    
    if df is not None:
        st.write(df)

# Função principal
def main():
    st.title('Análise de Produção Científica')
    st.sidebar.header('Opções')

    # Mostrar opções para análise
    opcao = st.sidebar.selectbox('Selecione uma opção:', ['Contagem por Ano da Publicação',
                                                         'Contagem por Categoria',
                                                         'Contagem por Tipo de Produção',
                                                         'Contagem por Área de Concentração',
                                                         'Contagem por Linha de Pesquisa',
                                                         'Mostrar Autores por Título',
                                                         'Produção Relevante de Egresso'])

    # Executar a análise com base na opção selecionada
    if opcao == 'Contagem por Ano da Publicação':
        contagem_por_ano()
    elif opcao == 'Contagem por Categoria':
        contagem_por_categoria()
    elif opcao == 'Contagem por Tipo de Produção':
        contagem_por_tipo_producao()
    elif opcao == 'Contagem por Área de Concentração':
        contagem_por_area_concentracao()
    elif opcao == 'Contagem por Linha de Pesquisa':
        contagem_por_linha_pesquisa()
    elif opcao == 'Mostrar Autores por Título':
        mostrar_autores_por_titulo()
    elif opcao == 'Produção Relevante de Egresso':
          mostrarprod_egresso()

if __name__ == '__main__':
        main()