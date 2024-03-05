import streamlit as st
import psycopg2
import pandas as pd
import os
import subprocess

# Estilo da barra azul
st.markdown(
    """
    <style>
        .barra-azul {
            background-color: #0b0b64;
            padding: 10px;
            color: white;
            font-size: 24px;
            text-align: center;
            border-radius: 15px;
            margin-bottom: 20px;
        }
    </style>
    <div class="barra-azul">PLANO ESTRATÉGICO DA ADMINISTRAÇÃO</div>
    """,
    unsafe_allow_html=True
)


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

#####
def obter_objetivos():
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome FROM objetivo_adm")  
        objetivos = cursor.fetchall()
        return objetivos
    except psycopg2.Error as e:
        st.error("Erro ao obter objetivos: {}".format(e))
        return []

def obter_metas(objetivo_id):
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome FROM meta_adm WHERE objetivo_id = %s", (objetivo_id,))  
        metas = cursor.fetchall()
        return metas
    except psycopg2.Error as e:
        st.error("Erro ao obter metas: {}".format(e))
        return []

# Obtém os objetivos
objetivos = obter_objetivos()

# Mostra os objetivos em um dropdown
if objetivos:
    objetivo_escolhido = st.selectbox("Selecione um objetivo:", [objetivo[1] for objetivo in objetivos])

    # Obtém o ID do objetivo escolhido
    objetivo_id = [objetivo[0] for objetivo in objetivos if objetivo[1] == objetivo_escolhido][0]

    # Obtém as metas correspondentes ao objetivo escolhido
    metas = obter_metas(objetivo_id)

    # Mostra as metas correspondentes ao objetivo escolhido
    st.write("Metas correspondentes ao objetivo escolhido:")
    for meta in metas:
        st.write(meta[1])  # Aqui você pode exibir os detalhes das metas, se necessário
else:
    st.warning("Não há objetivos disponíveis. Por favor, cadastre um objetivo primeiro.")