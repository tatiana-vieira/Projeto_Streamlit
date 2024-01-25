import streamlit as st
import pandas as pd
import psycopg2

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
        print("Erro ao conectar ao banco de dados:", e)
        return None
    
    cursor = conn.cursor()
#return conn, cursor

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
            cur.execute("""
                CREATE TABLE IF NOT EXISTS acao_adm (
                    id SERIAL PRIMARY KEY,
                    indicador_id INTEGER REFERENCES indicador_adm(id),
                    descricao TEXT NOT NULL,
                    status VARCHAR(50) NOT NULL
                )
            """)

# Função para inserir dados
def inserir_objetivo(nome):
    # Exibindo objetivos existentes
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM objetivo_adm")
            resultados = cur.fetchall()
            objetivos_cadastrados = st.selectbox("Escolha um Objetivo:", [""] + [row[1] for row in resultados])

# Função para inserir dados
def inserir_objetivo(nome):
    # Exibindo objetivos existentes
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

def inserir_acao(indicador_id, descricao, status="A Fazer"):
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO acao_adm (indicador_id, descricao, status) VALUES (%s, %s, %s) RETURNING id", (indicador_id, descricao, status))
            return cur.fetchone()[0]

# Criar tabelas se não existirem
criar_tabelas()

# Página principal
st.title("Cadastro de Objetivos, Metas, Indicadores e Ações")

# Formulário para cadastrar objetivo
novo_objetivo = st.text_input("Novo Objetivo:")
if st.button("Cadastrar Objetivo") and novo_objetivo:
    objetivo_id = inserir_objetivo(novo_objetivo)
    st.success(f"Objetivo '{novo_objetivo}' cadastrado com sucesso! (ID: {objetivo_id})")

# Exibindo objetivos existentes
objetivos_cadastrados = st.selectbox("Escolha um Objetivo:", [""] + [row[1] for row in conectar().execute("SELECT * FROM objetivo_adm").fetchall()])
if objetivos_cadastrados:
    # Formulário para cadastrar meta
    nova_meta = st.text_input("Nova Meta:")
    if st.button("Cadastrar Meta") and nova_meta:
        meta_id = inserir_meta(objetivos_cadastrados, nova_meta)
        st.success(f"Meta '{nova_meta}' cadastrada com sucesso! (ID: {meta_id})")

        # Formulário para cadastrar indicador
        novo_indicador = st.text_input("Novo Indicador:")
        if st.button("Cadastrar Indicador") and novo_indicador:
            indicador_id = inserir_indicador(meta_id, novo_indicador)
            st.success(f"Indicador '{novo_indicador}' cadastrado com sucesso! (ID: {indicador_id})")

            # Formulário para cadastrar ação
            nova_acao_descricao = st.text_input("Descrição da Nova Ação:")
            if st.button("Cadastrar Ação") and nova_acao_descricao:
                acao_id = inserir_acao(indicador_id, nova_acao_descricao)
                st.success(f"Ação '{nova_acao_descricao}' cadastrada com sucesso! (ID: {acao_id})")

                # Exibir quadro Kanban com ações
                st.subheader("Quadro Kanban:")
                acoes_df = pd.DataFrame({"ID": [1, 2, 3], "Descrição": ["Ação 1", "Ação 2", "Ação 3"], "Status": ["A Fazer", "A Fazer", "A Fazer"]})  # Substitua com os dados reais do banco
                st.write(acoes_df)