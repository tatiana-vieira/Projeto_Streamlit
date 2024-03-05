import streamlit as st
import psycopg2
import pandas as pd

st.set_option('deprecation.showPyplotGlobalUse', False)

# Função para conectar ao banco de dados
def conectar():
    # Configurações do banco de dados
    dbname = "DB_PRPPG"
    user = "postgres"
    password = "1234"
    host = "localhost"
    port = "5432"

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

# Função para obter os objetivos do banco de dados
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
    finally:
        conn.close()

# Função para obter as metas de um objetivo específico do banco de dados
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
    finally:
        conn.close()

# Função para obter os indicadores de uma meta específica do banco de dados
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
    finally:
        conn.close()

# Obtém os objetivos
objetivos = obter_objetivos()

# Mostra os objetivos em um dropdown
if objetivos:
    objetivo_escolhido = st.sidebar.selectbox("Selecione um objetivo:", [objetivo[1] for objetivo in objetivos])

    # Obtém o ID do objetivo escolhido
    objetivo_id = [objetivo[0] for objetivo in objetivos if objetivo[1] == objetivo_escolhido][0]

    # Obtém as metas correspondentes ao objetivo escolhido
    metas = obter_metas(objetivo_id)

    # Verifica se existem metas associadas ao objetivo escolhido
    if metas:
        # Mostra as metas correspondentes ao objetivo escolhido
        st.sidebar.write("Metas correspondentes ao objetivo escolhido:")
        meta_escolhida = st.sidebar.selectbox("Selecione uma meta:", [meta[1] for meta in metas])

        # Obtém o ID da meta escolhida
        meta_id = [meta[0] for meta in metas if meta[1] == meta_escolhida][0]

        # Obtém os indicadores correspondentes à meta escolhida
        indicadores = obter_indicadores(meta_id)

        # Mostra os indicadores correspondentes à meta escolhida
        st.sidebar.write("Indicadores correspondentes à meta escolhida:")
        indicador_escolhido = st.sidebar.selectbox("Selecione um indicador:", [indicador[1] for indicador in indicadores])

        # Pergunta ao usuário se deseja cadastrar uma nova ação
        nova_acao = st.sidebar.button("Cadastrar Nova Ação")

        # Se o usuário deseja cadastrar uma nova ação
        if nova_acao:
            # Pede ao usuário para inserir a porcentagem realizada
            porcentagem_realizada = st.sidebar.slider("Porcentagem Realizada", 0, 100, 0)

            # Insere os dados da nova ação em um DataFrame
            nova_acao_data = {
                "Objetivo": [objetivo_escolhido],
                "Meta": [meta_escolhida],
                "Indicador": [indicador_escolhido],
                "Porcentagem Realizada": [porcentagem_realizada]
            }

            # Adiciona a nova ação ao DataFrame de ações
            df_acoes = pd.DataFrame(nova_acao_data)

            # Mostra o DataFrame de ações
            st.write("Ações:")
            st.write(df_acoes)

        else:
            # Carrega as ações existentes do banco de dados
            # Isso deve ser feito ao invés de criar manualmente como fizemos com "nova_acao_data"
            # df_acoes = carregar_acoes_do_banco_de_dados()
            # Mostra o DataFrame de ações
            # st.write("Ações:")
            # st.write(df_acoes)
            st.warning("Nenhuma ação cadastrada ainda.")
    else:
        st.warning("Não há metas correspondentes ao objetivo escolhido.")
else:
    # Se não houver objetivos disponíveis, informa ao usuário
    st.warning("Não há objetivos disponíveis.")

# Função para exibir a tabela de ações
def mostrar_tabela_acoes(objetivo, meta, indicador):
    # Define as colunas da tabela
    colunas = ["Objetivo", "Meta", "Indicador", "Ação", "Estado"]
    
    # Cria um DataFrame vazio para armazenar as ações
    df_acoes = pd.DataFrame(columns=colunas)
    
    # Adiciona os dados selecionados à tabela
    df_acoes.loc[0] = [objetivo, meta, indicador, "", "A Fazer"]
    
    # Mostra a tabela na interface
    st.write(df_acoes)

# Título da página
st.title("Cadastro de Ações")

# Seleção do objetivo
objetivo = st.selectbox("Selecione o Objetivo:", ["Objetivo 1", "Objetivo 2", "Objetivo 3"])

# Seleção da meta
meta = st.selectbox("Selecione a Meta:", ["Meta 1", "Meta 2", "Meta 3"])

# Seleção do indicador
indicador = st.selectbox("Selecione o Indicador:", ["Indicador 1", "Indicador 2", "Indicador 3"])

# Botão para cadastrar a ação
if st.button("Cadastrar Ação"):
    # Exibe a tabela de ações com os dados selecionados
    mostrar_tabela_acoes(objetivo, meta, indicador)

# Função para exibir o quadro de tarefas
# Função para exibir o quadro de tarefas
def mostrar_quadro_tarefas(objetivo, meta, indicador):
    # Cria um DataFrame vazio para o quadro de tarefas
    quadro_tarefas = pd.DataFrame(columns=["Ação", "Estado"])

    # Mostra o título do quadro de tarefas
    st.subheader("Quadro de Tarefas")

    # Adiciona as colunas do objetivo, meta e indicador ao quadro de tarefas
    st.write("Objetivo: ", objetivo)
    st.write("Meta: ", meta)
    st.write("Indicador: ", indicador)

    # Mostra o quadro de tarefas
    st.write(quadro_tarefas)

    # Adiciona um campo para cadastrar uma nova ação
    nova_acao = st.text_input("Cadastrar Nova Ação")
    if nova_acao:
        # Adiciona a nova ação ao quadro de tarefas
        quadro_tarefas = quadro_tarefas.append({"Ação": nova_acao, "Estado": "A Fazer"}, ignore_index=True)
        st.write(quadro_tarefas)

# Aplicativo principal
def main():
    # Chama a função para exibir o quadro de tarefas
    mostrar_quadro_tarefas("Objetivo 1", "Meta 1", "Indicador 1")  # Valores fictícios para demonstração

if __name__ == "__main__":
    main()