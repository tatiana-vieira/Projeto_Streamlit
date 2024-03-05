import streamlit as st
import psycopg2
import subprocess
import pandas as pd  # Adicionando a importação do Pandas

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

def obter_indicadores(meta_id):
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome FROM indicador_adm WHERE meta_id = %s", (meta_id,))  
        indicadores = cursor.fetchall()
        return indicadores
    except psycopg2.Error as e:
        st.error("Erro ao obter indicadores: {}".format(e))
        return []

def cadastrar_acao(id_indicador, descricao, status):
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO acao_adm (id_indicador, descricao, status) VALUES (%s, %s, %s)", (id_indicador, descricao, status))
        conn.commit()
        st.success("A ação foi cadastrada com sucesso!")
    except psycopg2.Error as e:
        conn.rollback()
        st.error("Erro ao cadastrar ação: {}".format(e))
    finally:
        fechar_conexao(conn)

# Função para fechar a conexão com o banco de dados
def fechar_conexao(conn):
    if conn:
        conn.close()

# Obtém os objetivos
objetivos = obter_objetivos()

# Mostra os objetivos em um dropdown
if objetivos:
    objetivo_escolhido = st.selectbox("Selecione um objetivo:", [objetivo[1] for objetivo in objetivos])

    # Obtém o ID do objetivo escolhido
    objetivo_id = [objetivo[0] for objetivo in objetivos if objetivo[1] == objetivo_escolhido][0]

    # Botão para cadastrar objetivos
    if st.button("Cadastrar Objetivo"):
        # Aqui você pode adicionar a lógica para cadastrar objetivos
        pass

    # Obtém as metas correspondentes ao objetivo escolhido
    metas = obter_metas(objetivo_id)

    # Verifica se existem metas associadas ao objetivo escolhido
    if metas:
        # Mostra as metas correspondentes ao objetivo escolhido
        st.write("Metas correspondentes ao objetivo escolhido:")
        metas_nomes = [meta[1] for meta in metas]
        meta_escolhida = st.selectbox("Selecione uma meta:", metas_nomes)

        # Botão para cadastrar indicadores
        if st.button("Cadastrar Indicador"):
            # Aqui você pode adicionar a lógica para cadastrar indicadores
            pass

        # Obtém o ID da meta escolhida
        meta_id = [meta[0] for meta in metas if meta[1] == meta_escolhida][0]

        # Obtém os indicadores correspondentes à meta escolhida
        indicadores = obter_indicadores(meta_id)

        # Mostra os indicadores correspondentes à meta escolhida em uma tabela
        if indicadores:
            st.write("Indicadores correspondentes à meta escolhida:")
            df_indicadores = pd.DataFrame(indicadores, columns=["ID", "Nome"])
            st.dataframe(df_indicadores)

            # Pega o ID do indicador selecionado pelo usuário
            indicador_selecionado = st.selectbox("Selecione um indicador:", df_indicadores["Nome"])

            # Obtém o ID do indicador escolhido
            id_indicador = df_indicadores[df_indicadores["Nome"] == indicador_selecionado]["ID"].values[0]

            # Adiciona a funcionalidade de cadastrar ações quando o usuário clicar em um indicador
            st.write(f"Você selecionou o indicador: {indicador_selecionado}")
            descricao = st.text_input("Descrição da Ação:")
            status = st.radio("Status:", ["A Fazer", "Em Andamento", "Concluído"])
            if st.button("Cadastrar Ação"):
                cadastrar_acao(id_indicador, descricao, status)
                st.experimental_rerun()
        else:
            st.warning("Não há indicadores associados à meta escolhida.")
    else:
        # Se não houver metas associadas, pergunte ao usuário se deseja cadastrar uma
        resposta = st.radio("Não há metas associadas ao objetivo escolhido. Deseja cadastrar uma meta?", ("Sim", "Não"))
        if resposta == "Sim":
            if st.button("Cadastrar Meta"):
                subprocess.run(["streamlit", "run", "c:/Users/thatt/Documents/Projeto_Streamlit/src/meta.py"])
else:
    st.warning("Não há objetivos disponíveis. Por favor, cadastre um objetivo primeiro.")