import streamlit as st
import psycopg2
import pandas as pd
import os
import subprocess

def conectar():
    # Configurações do banco de dados
    dbname = "DB_PRPPG"
    user = "postgres"
    password = "1234"
    host = "localhost"
    port = "5432"  # Normalmente, a porta padrão é 5432

    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        return conn

    except psycopg2.Error as e:
        st.error("Erro ao conectar ao banco de dados: {}".format(e))
        return None

def fechar_conexao(conn):
    if conn:
        conn.close()

def obter_metas():
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome FROM meta_adm")  # Substitua 'tabela_objetivo' pelo nome correto da sua tabela de objetivos
        metas = cursor.fetchall()
        return metas
    except psycopg2.Error as e:
        st.error("Erro ao obter metas: {}".format(e))
        return []

def obter_indicadores():
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, meta_id FROM indicador_adm")  # Substitua 'indicador_adm' pelo nome correto da sua tabela de indicadores
        indicadores = cursor.fetchall()
        return indicadores
    except psycopg2.Error as e:
        st.error("Erro ao obter Indicadores: {}".format(e))
        return []

def cadastrar_indicador(id_indicador, nome_indicador, id_meta):
    conn = conectar()
    try:
        cursor = conn.cursor()
        # Substitua 'sua_tabela_meta' pelo nome correto da sua tabela de metas
        cursor.execute("INSERT INTO indicador_adm (id, nome, meta_id) VALUES (%s, %s, %s)", (id_indicador, nome_indicador, id_meta))
        conn.commit()
        
        st.success("O indicador foi cadastrado com sucesso!")
    except psycopg2.Error as e:
        conn.rollback()
        st.error("Erro ao cadastrar indicador: {}".format(e))
    finally:
        fechar_conexao(conn)

st.title("Cadastro de Indicador")

# Campos do formulário
id_indicador = st.text_input("ID do indicador")
nome_indicador = st.text_input("Nome do indicador")

# Obter lista de metas
metas = obter_metas()
opcoes_metas = {meta[1]: meta[0] for meta in metas}
meta_selecionada = st.selectbox("Selecione a meta", list(opcoes_metas.keys()))

# Verificar se o ID da meta foi obtido com sucesso antes de prosseguir
if meta_selecionada in opcoes_metas:
    id_meta_selecionada = opcoes_metas[meta_selecionada]

    # Obter e mostrar os indicadores existentes em um DataFrame
    indicadores_existentes = obter_indicadores()
    df_indicadores = pd.DataFrame(indicadores_existentes, columns=["id", "nome", "meta_id"])
    st.write("Indicadores existentes:")
    st.write(df_indicadores)

    # Chamar a função de cadastrar_indicador com os parâmetros corretos
    cadastrar_indicador(id_indicador, nome_indicador, id_meta_selecionada)
else:
    st.warning("Selecione uma meta válida antes de cadastrar um indicador.")    

# Botão Voltar
if st.button("Voltar"):
    subprocess.run(["streamlit", "run", "c:/Users/thatt/Documents/Projeto_Streamlit/src/teste.py"])