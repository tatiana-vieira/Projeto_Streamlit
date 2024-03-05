import streamlit as st
import psycopg2
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

def cadastrar_objetivo():
    st.title("Cadastro de Objetivo")
    
    # Campos do formulário
    id_objetivo = st.text_input("ID do Objetivo")
    nome_objetivo = st.text_input("Nome do Objetivo")

    # Botão para cadastrar
    if st.button("Cadastrar"):
        conn = conectar()
        try:
            cursor = conn.cursor()

            # Execute a inserção na tabela
            cursor.execute("INSERT INTO objetivo_adm (id, nome) VALUES (%s, %s)", (id_objetivo, nome_objetivo))

            # Commit para efetivar a inserção
            conn.commit()

            st.success("Objetivo cadastrado com sucesso!")
        except psycopg2.Error as e:
            st.error(f"Erro ao cadastrar objetivo: {e}")
        finally:
            fechar_conexao(conn)

# Executa a função de cadastro
cadastrar_objetivo()
if st.button ("Voltar"):
      subprocess.run(["streamlit", "run", "c:/Users/thatt/Documents/Projeto_Streamlit/src/teste.py"]) 