import streamlit as st
import pandas as pd
import psycopg2

# Definir funções

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
        cursor = conn.cursor()
        return conn, cursor

    except psycopg2.Error as e:
        print("Erro ao conectar ao banco de dados:", e)
        return None, None  # Retorna uma tupla vazia se houver erro

def fechar_conexao(conn, cursor):
    if conn:
        conn.close()
    if cursor:
        cursor.close()

# Função para obter dados do banco de dados
def obter_dados(query):
    conn, cursor = conectar()
    try:
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=columns)
        return df
    finally:
        fechar_conexao(conn, cursor)

def inserir_acao(indicador_id, descricao, status):
    # Conecte-se ao banco de dados e insira a nova ação
    conn, cursor = conectar()
    try:
        cursor.execute("INSERT INTO acao_adm (indicador_id, descricao, status) VALUES (%s, %s, %s)",
                       (indicador_id, descricao, status))
        conn.commit()
    finally:
        fechar_conexao(conn, cursor)

def obter_acoes(indicador_id):
    # Conecte-se ao banco de dados e obtenha as ações associadas ao indicador
    conn, cursor = conectar()
    try:
        cursor.execute("SELECT * FROM acao_adm WHERE indicador_id = %s", (indicador_id,))
        columns = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=columns)
        return df
    finally:
        fechar_conexao(conn, cursor)

# Restante do código...

# Consultas SQL para obter dados
query_objetivo = "SELECT * FROM objetivo_adm"
query_meta = "SELECT meta_adm.nome FROM meta_adm JOIN objetivo_adm ON objetivo_adm.id = meta_adm.objetivo_id"
query_indicador = "SELECT indicador_adm.nome, indicador_adm.id FROM indicador_adm JOIN meta_adm ON meta_adm.id = indicador_adm.meta_id"

# Obtendo dados do banco
df_objetivo = obter_dados(query_objetivo)
df_meta = obter_dados(query_meta)
df_indicador = obter_dados(query_indicador)

# Adicione este comando para visualizar o DataFrame df_meta
print(df_meta)

# Organizando os dados para o Kanban
objetivo_dict = {row["nome"]: row for _, row in df_objetivo.iterrows()}
meta_dict = {row["nome"]: row for _, row in df_meta.iterrows()}
indicador_dict = {row["nome"]: row for _, row in df_indicador.iterrows()}

# Criando as colunas do Kanban
col_objetivo, col_meta, col_indicador = st.columns(3)

# Adicionando títulos
with col_objetivo:
    st.header("Objetivo")
with col_meta:
    st.header("Meta")
with col_indicador:
    st.header("Indicador")

# Preenchendo as colunas com os cartões do Kanban
with col_objetivo:
    for _, objetivo in objetivo_dict.items():
        st.info(f"**{objetivo['nome']}")

with col_meta:
    for _, meta in meta_dict.items():
        st.info(f"**{meta['nome']}")

with col_indicador:
    for _, indicador in indicador_dict.items():
        st.info(f"**{indicador['nome']}")

# Adicione um formulário para escolher um indicador
indicador_selecionado = st.selectbox("Escolha um Indicador:", list(indicador_dict.keys()))

# Adicione um formulário para inserir ações
nova_acao = st.text_input("Nova Ação:")
status_acao = st.selectbox("Status da Ação:", ["Fazer", "Executar", "Ajustar", "Feito"])

if st.button("Adicionar Ação"):
    # Insira a nova ação no banco de dados associada ao indicador selecionado
    inserir_acao(indicador_dict[indicador_selecionado]["id"], nova_acao, status_acao)

# Exiba as ações associadas ao indicador selecionado
st.header("Ações:")
exibir_acoes(indicador_dict[indicador_selecionado]["id"])

def exibir_acoes(indicador_id):
    # Obtenha as ações associadas ao indicador
    df_acoes = obter_acoes(indicador_id)
    
    # Exiba as ações
    st.table(df_acoes)

def exibir_acoes(indicador_id):
    # Obtenha as ações associadas ao indicador
    df_acoes = obter_acoes(indicador_id)
    
    # Exiba as ações
    st.table(df_acoes)

    # Adicione um formulário para alterar o status
    acao_selecionada = st.selectbox("Escolha uma Ação:", df_acoes["descricao"].tolist())
    novo_status = st.selectbox("Novo Status:", ["Fazer", "Executar", "Ajustar", "Feito"])

    if st.button("Atualizar Status"):
        # Atualize o status da ação no banco de dados
        atualizar_status_acao(acao_selecionada, novo_status)

    # Calcule e exiba a porcentagem de conclusão
    total_acoes = len(df_acoes)
    acoes_feitas = len(df_acoes[df_acoes["status"] == "Feito"])
    porcentagem_conclusao = (acoes_feitas / total_acoes) * 100

    st.text(f"Porcentagem de Conclusão: {porcentagem_conclusao:.2f}%")

# ...

def atualizar_status_acao(descricao_acao, novo_status):
    # Conecte-se ao banco de dados e atualize o status da ação
    conn, cursor = conectar()
    try:
        cursor.execute("UPDATE acao_adm SET status = %s WHERE descricao = %s",
                       (novo_status, descricao_acao))
        conn.commit()
    finally:
        fechar_conexao(conn, cursor)