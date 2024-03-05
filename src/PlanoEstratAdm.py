import streamlit as st
import pandas as pd
import psycopg2
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

# Função para conectar ao banco de dados
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

# Função para fechar a conexão
def fechar_conexao(conn):
    if conn:
        conn.close()

# Função para executar consultas
def executar_consulta(query):
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=columns)
        return df
    finally:
        fechar_conexao(conn)

# Função para cadastrar uma meta
def cadastrar_meta(id_meta, nome_meta, id_objetivo):
    conn = conectar()
    try:
        cursor = conn.cursor()
        subprocess.run(["streamlit", "run", "c:/Users/thatt/Documents/Projeto_Streamlit/src/metas-adm.py"])
    except psycopg2.Error as e:
        conn.rollback()
        st.error("Erro ao cadastrar meta: {}".format(e))
    finally:
        fechar_conexao(conn)

# Consulta para obter dados da tabela objetivo_adm
consulta_objetivo = "SELECT nome FROM objetivo_adm"
dados_objetivo = executar_consulta(consulta_objetivo)

# Verifica se dados_objetivo está vazio antes de usar em st.selectbox
if not dados_objetivo.empty:
    # Adicionar selectbox à barra lateral
    tabela_selecionada = st.sidebar.selectbox("Selecione um Objetivo:", dados_objetivo)

    # Adicionar botão de cadastro à barra lateral
    if st.sidebar.button("Cadastrar Objetivo"):
        # Abre a página de cadastro de objetivos
        subprocess.run(["streamlit", "run", "c:/Users/thatt/Documents/Projeto_Streamlit/src/cadastros_adm.py"])

    # Seção para mostrar as metas do objetivo selecionado
    st.sidebar.markdown(f"<h2>Metas do Objetivo '{tabela_selecionada}':</h2>", unsafe_allow_html=True)

    # Adicionar botão de cadastro para Meta
    if st.sidebar.button("Cadastrar Meta"):
        # Adicione aqui a lógica para cadastrar uma nova Meta no banco de dados
        subprocess.run(["streamlit", "run", "c:/Users/thatt/Documents/Projeto_Streamlit/src/cadastros_adm.py"])

    # Consulta para obter dados da tabela meta_adm correspondentes ao objetivo selecionado
    consulta_meta = f"SELECT meta_adm.nome FROM objetivo_adm JOIN meta_adm ON objetivo_adm.id = meta_adm.objetivo_id WHERE objetivo_adm.nome = '{tabela_selecionada}'"
    dados_meta = executar_consulta(consulta_meta)
    st.sidebar.dataframe(dados_meta)

    # Adicionar botão de cadastro para Indicador
    if st.sidebar.button("Cadastrar Indicador"):
        # Adicione aqui a lógica para cadastrar um novo Indicador no banco de dados
        subprocess.run(["streamlit", "run", "c:/Users/thatt/Documents/Projeto_Streamlit/src/cadastros_adm.py"])






