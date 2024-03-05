import streamlit as st
from utils.conexao_db import conectar, fechar_conexao

# Função para criar tabelas
def criar_tabelas():
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS objetivo_adm (
                    id SERIAL PRIMARY KEY,
                    nome VARCHAR(255) NOT NULL
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS meta_adm (
                    id SERIAL PRIMARY KEY,
                    objetivo_id INTEGER REFERENCES objetivo_adm(id),
                    nome VARCHAR(255) NOT NULL
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS indicador_adm (
                    id SERIAL PRIMARY KEY,
                    meta_id INTEGER REFERENCES meta_adm(id),
                    nome VARCHAR(255) NOT NULL
                )
            """)

# Função para inserir dados
def inserir_objetivo(nome):
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO objetivo_adm (nome) VALUES (%s) RETURNING id", (nome,))
            return cur.fetchone()[0]

def inserir_meta(objetivo_id, nome):
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO meta_adm (objetivo_id, nome) VALUES (%s, %s) RETURNING id", (objetivo_id, nome))
            return cur.fetchone()[0]

def inserir_indicador(meta_id, nome):
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO indicador_adm (meta_id, nome) VALUES (%s, %s) RETURNING id", (meta_id, nome))
            return cur.fetchone()[0]

# Criar tabelas se não existirem
criar_tabelas()

# Página principal
st.title("Cadastro de Objetivos, Metas e Indicadores")

# Formulário para cadastrar objetivo
novo_objetivo = st.text_input("Novo Objetivo:")
if st.button("Cadastrar Objetivo") and novo_objetivo:
    objetivo_id = inserir_objetivo(novo_objetivo)
    st.success(f"Objetivo '{novo_objetivo}' cadastrado com sucesso! (ID: {objetivo_id})")

# Exibindo objetivos existentes
objetivos_existentes = st.selectbox("Escolha um Objetivo:", [""] + ["Melhorar a qualidade do ensino", "Promover a Modernização dos Cursos", "Promover a Internacionalização do ensino"])
if objetivos_existentes:
    # Exibindo opções para cadastrar meta e indicador
    nova_meta = st.text_input("Nova Meta:")
    if st.button("Cadastrar Meta") and nova_meta:
        objetivo_id = 1  # Substitua com o valor correto obtido ao cadastrar o objetivo
        meta_id = inserir_meta(objetivo_id, nova_meta)
        st.success(f"Meta '{nova_meta}' cadastrada com sucesso! (ID: {meta_id})")

        # Exibindo opções para cadastrar indicador
        novo_indicador = st.text_input("Novo Indicador:")
        if st.button("Cadastrar Indicador") and novo_indicador:
            indicador_id = inserir_indicador(meta_id, novo_indicador)
            st.success(f"Indicador '{novo_indicador}' cadastrado com sucesso! (ID: {indicador_id})")

    # Exibindo indicadores vinculados à meta escolhida
    st.write("Indicadores Vinculados à Meta:")
    indicadores = ["Indicador 1", "Indicador 2"]  # Substitua com os indicadores reais
    for indicador in indicadores:
        st.write(f"- {indicador}")