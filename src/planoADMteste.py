import streamlit as st
import psycopg2
import subprocess
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.ticker as ticker


st.set_option('deprecation.showPyplotGlobalUse', False)

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
        metas_nomes = [meta[1] for meta in metas]
        meta_escolhida = st.sidebar.selectbox("Selecione uma meta:", metas_nomes)

        # Obtém o ID da meta escolhida
        meta_id = [meta[0] for meta in metas if meta[1] == meta_escolhida][0]

        # Obtém os indicadores correspondentes à meta escolhida
        indicadores = obter_indicadores(meta_id)

        # Mostra os indicadores correspondentes à meta escolhida
        st.sidebar.write("Indicadores correspondentes à meta escolhida:")
        for indicador in indicadores:
            st.sidebar.write(indicador[1])  # Aqui você pode exibir os detalhes dos indicadores, se necessário

            # Conectar ao banco de dados
            conn = conectar()
            cur = conn.cursor()

            try:
                if indicador[1] == 'Taxa de sucesso nos cursos':
                    # Consulta1: Contar o número de alunos matriculados por ano
                    cur.execute("""
                        SELECT anomatricula, COUNT(DISTINCT nome) 
                        FROM discente 
                        WHERE codigoprograma = '32003013014P4' 
                        GROUP BY anomatricula;
                    """)
                    resultados = cur.fetchall()
                    anos_matriculados = []
                    quantidade_alunos = []

                    for anomatricula, quantidade in resultados:
                        anos_matriculados.append(anomatricula)
                        quantidade_alunos.append(quantidade)

                    # Configurar o plot
                    fig, ax = plt.subplots()
                    ax.bar(anos_matriculados, quantidade_alunos)
                    ax.set_xlabel('Quantidade')
                    ax.set_ylabel('Matriculados por ano')

                    # Exibir o gráfico utilizando Streamlit
                    st.pyplot(fig)

                    # Consulta 2: Alunos que concluíram
                    cur.execute("SELECT anosituacao, COUNT(*) FROM discente WHERE situacao = 'TITULADO' and codigoprograma = '32003013014P4' GROUP BY anosituacao")
                    total_concluidos = cur.fetchall()

                    anos_situacao = [resultado[0] for resultado in total_concluidos]
                    quantidade_alunos_concluidos = [resultado[1] for resultado in total_concluidos]

                    # Configurar o plot
                    plt.figure(figsize=(10, 6))
                    plt.bar(anos_situacao, quantidade_alunos_concluidos, color='blue')
                    plt.xlabel('Ano de Conclusão')
                    plt.ylabel('Número de Alunos Concluídos')
                    plt.title('Número de Alunos que Concluíram por Ano')
                    plt.xticks(anos_situacao)  # Define os anos como os ticks do eixo x
                    plt.grid(True)

                    # Exibir o gráfico utilizando Streamlit
                    st.pyplot()

                    #consulta3:# Consulta: Tempo decorrido da matrícula até a conclusão (situação 'TITULADO')
                    cur.execute("""
                        SELECT 
                            nome,
                            anomatricula,
                            anosituacao,
                            anosituacao - anomatricula AS tempo_decorrido
                        FROM 
                            discente 
                        WHERE 
                            situacao = 'TITULADO' 
                            AND codigoprograma = '32003013014P4'
                    """)
                    resultados = cur.fetchall()

                    # Extrair os dados do resultado
                    nomes = [resultado[0] for resultado in resultados]
                    anos_matricula = [resultado[1] for resultado in resultados]
                    anos_conclusao = [resultado[2] for resultado in resultados]
                    tempo_decorrido = [resultado[3] for resultado in resultados]

                    # Configurar o plot
                    plt.figure(figsize=(10, 6))
                    plt.bar(nomes, tempo_decorrido, color='green')
                    plt.xlabel('Aluno')
                    plt.ylabel('Tempo Decorrido (Anos)')
                    plt.title('Tempo Decorrido da Matrícula até a Conclusão')
                    plt.xticks(rotation=90)  # Rotaciona os nomes dos alunos para melhor legibilidade
                    plt.grid(True)

                    # Exibir o gráfico utilizando Streamlit
                    st.pyplot()
                ############################################################################################
                if indicador[1] == 'Taxa de evasão':
                    # Executar a consulta para obter o total de alunos únicos para o código do programa especificado
                    cur.execute("""
                        SELECT COUNT(*) AS total_alunos
                        FROM (
                            SELECT DISTINCT nome 
                            FROM discente 
                            WHERE codigoprograma = '32003013014P4'
                        ) AS subquery;
                    """)
                    total_alunos = cur.fetchone()[0]

                    # Executar a consulta para obter o total de alunos que saíram (taxa de evasão)
                    cur.execute("""
                        SELECT COUNT(*) AS total_evasao
                        FROM discente
                        WHERE situacao = 'DESLIGADO' 
                        AND codigoprograma = '32003013014P4';
                    """)
                    total_evasao = cur.fetchone()[0]

                    # Calcular a taxa de evasão
                    taxa_evasao = (total_evasao / total_alunos) * 100

                    # Mostrar a taxa de evasão
                    st.write("Taxa de evasão:", taxa_evasao, "%")
                ##########################################################################################################################
                if indicador[1] == 'Número dos cursos':
                    # Consulta: Contar o número de alunos matriculados por ano
                    cur.execute("""
                        SELECT anomatricula, COUNT(DISTINCT nome) 
                        FROM discente 
                        WHERE codigoprograma = '32003013014P4' 
                        GROUP BY anomatricula;
                    """)
                    resultados = cur.fetchall()
                    anos_matriculados = []
                    quantidade_alunos = []

                    for anomatricula, quantidade in resultados:
                        anos_matriculados.append(anomatricula)
                        quantidade_alunos.append(quantidade)

                    # Configurar o plot
                    fig, ax = plt.subplots()
                    ax.bar(anos_matriculados, quantidade_alunos)
                    ax.set_xlabel('Ano de Matrícula')
                    ax.set_ylabel('Quantidade de Alunos')

                    # Exibir o gráfico utilizando Streamlit
                    st.pyplot(fig)

                    # Consulta 2: Alunos que concluíram
                    cur.execute("SELECT anosituacao, COUNT(*) FROM discente WHERE situacao = 'TITULADO' and codigoprograma = '32003013014P4' GROUP BY anosituacao")
                    total_concluidos = cur.fetchall()

                    # Consulta 3: Nivel e sexo
                    
                    # Consulta
                    cur.execute("SELECT nivel, sexo FROM discente WHERE codigoprograma = '32003013014P4'")
                    resultados = cur.fetchall()

                    # Criar um DataFrame com os resultados da consulta
                    df = pd.DataFrame(resultados, columns=['Nível', 'Sexo'])

                    # Configurar e exibir o gráfico utilizando Seaborn
                    plt.figure(figsize=(10, 6))
                    sns.countplot(data=df, x='Nível', hue='Sexo')
                    plt.title('Distribuição de Níveis por Sexo')
                    plt.xlabel('Nível')
                    plt.ylabel('Contagem')
                    plt.grid(True)
                    plt.legend(title='Sexo')
                    plt.xticks(rotation=45)  # Rotaciona os rótulos do eixo x para melhor legibilidade

                    # Exibir o gráfico utilizando Streamlit
                    st.pyplot()
                ########################################################################################################################
                if indicador[1] == 'Percentual de docentes com pós-doutorado':
                    try:
                        # Executar a consulta para obter os dados
                        cur.execute("""
                            SELECT nivel, COUNT(DISTINCT nome) as total_docentes
                            FROM docente 
                            WHERE codigoprograma = '32003013014P4' 
                            GROUP BY nivel
                            ORDER BY nivel;
                        """)
                        resultados = cur.fetchall()

                        # Transformar os resultados em um DataFrame
                        df_docentes = pd.DataFrame(resultados, columns=['Nível', 'Total de Docentes'])

                        # Criar um gráfico de barras
                        plt.figure(figsize=(10, 6))
                        plt.bar(df_docentes['Nível'], df_docentes['Total de Docentes'], color='skyblue')

                        # Configurar título e rótulos dos eixos
                        plt.title('Percentual de Docentes com Pós-Doutorado por Nível')
                        plt.xlabel('Nível')
                        plt.ylabel('Total de Docentes')

                        # Exibir o gráfico utilizando Streamlit
                        st.pyplot()

                    except psycopg2.Error as e:
                        st.error("Erro durante a execução da consulta: {}".format(e))
                ###########################################################################################################################
                if indicador[1] == 'Aumentar nota dos PPGs':
                    # 1- Consulta: Obter notas dos alunos no programa específico
                    cur.execute("SELECT DISTINCT nota, quadrienal FROM resultadoavaliacao WHERE codigoprograma = '32003013014P4' ORDER BY quadrienal")
                    resultados = cur.fetchall()

                                        # Executar a consulta e carregar os resultados em um DataFrame
                    df = pd.DataFrame(resultados, columns=['nota', 'quadrienal'])

                    
                    # Mostrar os resultados usando Streamlit
                    st.write("Resultados Avaliações da CAPES:")
                    st.write(df)
                # segunda consulta
                    consulta_quesitos = "select * from avaliacaoprog_adm"
                    cur.execute(consulta_quesitos)
                    dados_quesitos = cur.fetchall()
                                        
                                        # Exibir o DataFrame no Streamlit
                    df_quesitos = pd.DataFrame(dados_quesitos, columns=['Quesitos das Fichas de Avaliação', '2017', '2021'])
                    st.write(df_quesitos)
                ############################################################################################################3                    
                if indicador[1] == 'Índice H Scopus médio geral':
                    # Primeira consulta para gerar o primeiro gráfico de barras
                    consulta_sql = "SELECT nome,hscopus,hwebofscience FROM periodicos;"
                    try:
                        # Executar a primeira consulta e armazenar os resultados em um DataFrame
                        cur.execute(consulta_sql)
                        dados_periodicos = cur.fetchall()

                        # Transformar os resultados em um DataFrame
                        df_periodicos = pd.DataFrame(dados_periodicos, columns=['Nome', 'H index Scopus', 'H index Web'])

                        # Gerar o primeiro gráfico de barras comparando os h-indexes do Scopus e do Web para cada docente
                        fig, ax = plt.subplots(figsize=(10, 6))  # Cria a figura explicitamente
                        sns.barplot(data=df_periodicos, x='Nome', y='H index Scopus', color='blue', label='H index Scopus', ax=ax)
                        sns.barplot(data=df_periodicos, x='Nome', y='H index Web', color='red', label='H index Web', ax=ax)
                        ax.set_xlabel('Nome do Docente')
                        ax.set_ylabel('H-index')
                        ax.set_title('Comparação do h-index do Scopus e do Web por Docente')
                        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
                        ax.legend()

                        # Exibir o gráfico utilizando Streamlit
                        st.pyplot(fig)  # Passa a figura explicitamente para st.pyplot()
                    except psycopg2.Error as e:
                        st.error("Erro durante a execução da consulta: {}".format(e))

                    # Segunda consulta para gerar o segundo gráfico de barras
                    consulta_sql1 = "SELECT nome, documentoscopus, numpubliweb FROM periodicos;"
                    try:
                        # Executar a segunda consulta e armazenar os resultados em um DataFrame
                        cur.execute(consulta_sql1)
                        dados_periodicos = cur.fetchall()

                        # Transformar os resultados em um DataFrame
                        df_periodicos = pd.DataFrame(dados_periodicos, columns=['Nome', 'H index Scopus', 'Número de Publicações Web'])

                        # Gerar o segundo gráfico de barras comparando os H-indexes do Scopus e o número de publicações Web para cada docente
                        fig, ax = plt.subplots(figsize=(10, 6))
                        sns.barplot(data=df_periodicos, x='Nome', y='H index Scopus', color='blue', label='H index Scopus')
                        sns.barplot(data=df_periodicos, x='Nome', y='Número de Publicações Web', color='red', label='Número de Publicações Web')
                        ax.set_xlabel('Nome do Docente')
                        ax.set_ylabel('Valor')
                        ax.set_title('Comparação Número de Publicações por Docente')
                        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
                        ax.legend()
                        st.pyplot(fig)
                    except psycopg2.Error as e:
                        st.error("Erro durante a execução da segunda consulta: {}".format(e))
                    finally:
                        conn.close()  # Fechar conexão com o banco de dados após concluir todas as operações de consulta
                 ###################################################################################################################
                if indicador[1] == 'Numero de Produções Científicas qualificadas':
                    #primeira consulta
                    consulta_sql2 = "SELECT nome,hwebofscience,numpubliweb FROM periodicos;"
                    try:
                        # Executar a consulta e armazenar os resultados em um DataFrame
                        cur.execute(consulta_sql2)
                        dados_periodicos = cur.fetchall()
                        
                        # Transformar os resultados em um DataFrame
                        df_periodicos = pd.DataFrame(dados_periodicos, columns=['Nome', 'H Web of Science', 'Número de Publicações Web'])

                        # Gerar o gráfico de barras comparando H Web of Science e o número de publicações Web por docente
                        fig, ax = plt.subplots(figsize=(10, 6))
                        sns.barplot(data=df_periodicos, x='Nome', y='H Web of Science', color='blue', label='H Web of Science')
                        sns.barplot(data=df_periodicos, x='Nome', y='Número de Publicações Web', color='red', label='Número de Publicações Web')
                        ax.set_xlabel('Nome do Docente')
                        ax.set_ylabel('Valor')
                        ax.set_title('Comparação H Web of Science e Número de Publicações Web por Docente')
                        
                        # Definir os ticks manualmente ou usar FixedLocator
                        ax.xaxis.set_major_locator(ticker.FixedLocator(range(len(df_periodicos['Nome']))))
                        ax.set_xticklabels(df_periodicos['Nome'], rotation=45, ha='right')
                        
                        ax.legend()
                        
                        # Exibir o gráfico utilizando Streamlit
                        st.pyplot(fig)
                    except psycopg2.Error as e:
                        st.error("Erro durante a execução da consulta: {}".format(e))
                ##############################################################################################################################    
                if indicador[1] == 'Numero de Produções Científicas':
                    consulta_sql = "select orientacaointernmestrado, oportunidadeestudarexterior, doutaradointer, publconjintern, bolsapesquisaintern, Nome, Pais from orientacaointern where programa='Administracao';"
                    try:
                        # Executar a consulta e armazenar os resultados em um DataFrame
                        conn = conectar()  # Estabelecer a conexão com o banco de dados
                        cur = conn.cursor()
                        cur.execute(consulta_sql)
                        dados_orientacao = cur.fetchall()
                        
                        # Transformar os resultados em um DataFrame
                        df_orientacao = pd.DataFrame(dados_orientacao, columns=['Orientacao Mestrado', 'Oportunidade estudar no exterior', 'Doutorado Internacional', 'Publicacao Conjunta Internacional', 'Bolsa pesquisa', 'Nome', 'Pais'])

                        # Criar um gráfico de dispersão
                        plt.figure(figsize=(10, 6))
                        plt.scatter(df_orientacao['Nome'], df_orientacao['Orientacao Mestrado'], color='red', label='Orientação Mestrado', alpha=0.5)
                        plt.scatter(df_orientacao['Nome'], df_orientacao['Oportunidade estudar no exterior'], color='blue', label='Oportunidade estudar no exterior', alpha=0.5)
                        plt.scatter(df_orientacao['Nome'], df_orientacao['Doutorado Internacional'], color='green', label='Doutorado Internacional', alpha=0.5)
                        plt.scatter(df_orientacao['Nome'], df_orientacao['Publicacao Conjunta Internacional'], color='orange', label='Publicação Conjunta Internacional', alpha=0.5)
                        plt.scatter(df_orientacao['Nome'], df_orientacao['Bolsa pesquisa'], color='purple', label='Bolsa pesquisa', alpha=0.5)

                        # Configurar título e rótulos dos eixos
                        plt.title('Dados de Orientação e Pesquisa')
                        plt.xlabel('Nome')

                        plt.ylabel('Valor')
                        plt.xticks(rotation=90)


                        # Exibir a legenda
                        plt.legend()

                        # Exibir o gráfico utilizando Streamlit
                        st.pyplot()

                    except psycopg2.Error as e:
                        st.error("Erro durante a execução da consulta: {}".format(e))
                    finally:
                        if conn is not None:
                            conn.close()  # Fechar conexão com o banco de dados após c
               ################################################################################################################################
                if indicador[1] == 'Aumentar o valor financeiro':

                   consulta_bolsa= "SELECT nome,receitapesquisaexterna from pesquisar where programa='Administracao';"
                   try:
                        # Executar a consulta para obter os dados
                        cur.execute("""
                            SELECT nome, receitapesquisaexterna
                            FROM pesquisar
                            WHERE programa = 'Administracao';
                        """)
                        resultados = cur.fetchall()

                        # Transformar os resultados em um DataFrame
                        df_pesquisa = pd.DataFrame(resultados, columns=['Nome', 'Receita de Pesquisa Externa'])

                        # Criar um gráfico de barras
                        plt.figure(figsize=(10, 6))
                        plt.bar(df_pesquisa['Nome'], df_pesquisa['Receita de Pesquisa Externa'], color='skyblue')

                        # Configurar título e rótulos dos eixos
                        plt.title('Receita de Pesquisa Externa Internacional por Projeto')
                        plt.xlabel('Projeto')
                        plt.ylabel('Receita (em alguma unidade monetária)')

                        # Rotacionar os rótulos do eixo x
                        plt.xticks(rotation=90)

                        # Exibir o gráfico utilizando Streamlit
                        st.pyplot()
                   
                   except psycopg2.Error as e:
                        st.error("Erro durante a execução da segunda consulta: {}".format(e))
                   finally:
                        conn.close()  # Fechar conexão com o banco de dados após concluir todas as operações de consulta

                ##########################################################################################################################
                if indicador[1] == 'Percentual de docentes credenciados':
                    try:
                        # Executar a consulta para obter os dados
                        cur.execute("""
                            SELECT categoria, COUNT(DISTINCT nome) as total_docentes
                            FROM docente 
                            WHERE codigoprograma = '32003013014P4' 
                            GROUP BY categoria;
                        """)
                        resultados = cur.fetchall()

                        # Transformar os resultados em um DataFrame
                        df_docentes = pd.DataFrame(resultados, columns=['Categoria', 'Total de Docentes'])

                        # Criar o gráfico de pizza
                        fig, ax = plt.subplots()
                        ax.pie(df_docentes['Total de Docentes'], labels=df_docentes['Categoria'], autopct='%1.1f%%', startangle=90)
                        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

                        # Configurar título
                        ax.set_title('Percentual de Docentes Credenciados por Categoria')

                        # Exibir o gráfico utilizando Streamlit
                        st.pyplot(fig)

                        # Fechar conexão com o banco de dados
                        conn.close()
                    except psycopg2.Error as e:
                        st.error("Erro durante a execução da segunda consulta: {}".format(e))
                    finally:
                        conn.close()  # Fechar conexão com o banco de dados após concluir todas as operações de consulta
            

     ##############################################################################################################################
            #Número discentes e docentes pesquisadores
                if indicador[1] == 'Número de revisões estruturantes nos PPCs':
                    try:
                        # Executar a consulta para obter os dados
                        cur.execute("""
                            SELECT categoria, COUNT(DISTINCT nome) as total_docentes
                            FROM docente 
                            WHERE codigoprograma = '32003013014P4' 
                            GROUP BY categoria;
                        """)
                        resultados = cur.fetchall()

                        # Transformar os resultados em um DataFrame
                        df_docentes = pd.DataFrame(resultados, columns=['Categoria', 'Total de Docentes'])

                        # Criar o gráfico de pizza
                        fig, ax = plt.subplots()
                        ax.pie(df_docentes['Total de Docentes'], labels=df_docentes['Categoria'], autopct='%1.1f%%', startangle=90)
                        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

                        # Configurar título
                        ax.set_title('Percentual de Docentes Credenciados por Categoria')

                        # Exibir o gráfico utilizando Streamlit
                        st.pyplot(fig)

                        # Fechar conexão com o banco de dados
                        conn.close()
                    except psycopg2.Error as e:
                        st.error("Erro durante a execução da segunda consulta: {}".format(e))
                    finally:
                        conn.close()  # Fechar conexão com o banco de dados após concluir todas as operações de consulta
            except psycopg2.Error as e:
                    st.error("Erro durante a execução da segunda consulta: {}".format(e))
            finally:
                conn.close()  # Fechar conexão com o banco de dados após concluir todas as operações de consulta


    ##################################################################################################################################
else:
    # Se não houver metas associadas, pergunte ao usuário se deseja cadastrar uma
    resposta = st.sidebar.radio("Não há metas associadas ao objetivo escolhido. Deseja cadastrar uma meta?", ("Sim", "Não"))
    if resposta == "Sim":
        if st.sidebar.button("Cadastrar Meta"):
            subprocess.run(["streamlit", "run", "c:/Users/thatt/Documents/Projeto_Streamlit/src/meta.py"])
        else:
            st.warning("Não há objetivos disponíveis. Por favor, cadastre um objetivo primeiro.")
    else:
        st.warning("Não há objetivos disponíveis.")