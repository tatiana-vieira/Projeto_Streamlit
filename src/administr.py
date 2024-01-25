import streamlit as st
import pandas as pd
import plotly.express as px
from utils.conexao_db import conectar, fechar_conexao
import matplotlib.pyplot as plt

# Função para obter os dados da consulta
def obter_dados(conn, consulta):
    cursor = None

    try:
        if conn:
            cursor = conn.cursor()

            # Executar a consulta
            cursor.execute(consulta)
            dados = cursor.fetchall()

            # Obter os nomes das colunas
            colunas = [desc[0] for desc in cursor.description]

            return dados, colunas

    except Exception as e:
        print(f"Erro durante a execução da consulta: {e}")
        return (), ()  # Retorna uma tupla vazia

    finally:
        # Certifique-se de fechar o cursor quando terminar
        if cursor:
            cursor.close()

# Conectar ao banco de dados
conn = conectar()

# Verificar se a conexão foi bem-sucedida
if conn:
    st.title('Visualização de Dados')

    # Executar a primeira consulta
    consulta_ensinoaprendiz1 = "SELECT * FROM public.ensinoaprendiz1;"
    ensinoaprendiz1, colunas_ensinoaprendiz1 = obter_dados(conn, consulta_ensinoaprendiz1)

    # Mostrar os resultados na página
    st.header('Ensino Aprendizagem 1')
    st.dataframe(pd.DataFrame(ensinoaprendiz1, columns=colunas_ensinoaprendiz1))

    # Executar a segunda consulta
    consulta_orientacaointern = "SELECT * FROM public.orientacaointern;"
    orientacaointern, colunas_orientacaointern = obter_dados(conn, consulta_orientacaointern)

    # Mostrar os resultados na página
    st.header('Orientação Interna')
    st.dataframe(pd.DataFrame(orientacaointern, columns=colunas_orientacaointern))

    # Executar a terceira consulta
    consulta_transfconhecimento = "SELECT * FROM public.transfconhecimento;"
    transfconhecimento, colunas_transfconhecimento = obter_dados(conn, consulta_transfconhecimento)

    # Mostrar os resultados na página
    st.header('Transferência de Conhecimento')
    st.dataframe(pd.DataFrame(transfconhecimento, columns=colunas_transfconhecimento))

    # Executar a quarta consulta
    consulta_pesquisar= "SELECT * FROM public.pesquisar;"
    pesquisar, colunas_pesquisar = obter_dados(conn, consulta_pesquisar)

    # Mostrar os resultados na página
    st.header('Pesquisar')
    st.dataframe(pd.DataFrame(pesquisar, columns=colunas_pesquisar))

    # Fechar a conexão
    #fechar_conexao(conn)

# Verificar se a conexão foi bem-sucedida
# Verificar se a conexão foi bem-sucedida
if conn:
    # Executar a primeira consulta
    consulta_ensinoaprendiz1 = "SELECT nome, pais, mestradotempocerto FROM public.ensinoaprendiz1;"
    
    ensinoaprendiz1, colunas_ensinoaprendiz1 = obter_dados(conn, consulta_ensinoaprendiz1)

    # Mostrar os resultados na página
    st.title('Gráfico de Mapa: Ensino Aprendizagem 1')
    
    df_ensinoaprendiz1 = pd.DataFrame(ensinoaprendiz1, columns=colunas_ensinoaprendiz1)

    # Preencher valores NaN com zero
    df_ensinoaprendiz1['mestradotempocerto'] = pd.to_numeric(df_ensinoaprendiz1['mestradotempocerto'], errors='coerce').fillna(0)
    
    # Criar o gráfico de mapa usando plotly
    fig = px.scatter_geo(df_ensinoaprendiz1, locations='pais', locationmode='country names', color='mestradotempocerto', hover_name='nome', size='mestradotempocerto', projection='natural earth')

    # Adicionar detalhes ao gráfico
    fig.update_geos(showcoastlines=True, coastlinecolor="Black", showland=True, landcolor="white")
    fig.update_layout(title_text='Ensino Aprendizagem 1 - Mapa de Mestrado Tempo Certo')

    # Mostrar o gráfico na página do Streamlit
    st.plotly_chart(fig)
    

    # Fechar a conexão
    fechar_conexao(conn)