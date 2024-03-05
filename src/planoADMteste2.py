import streamlit as st
import psycopg2
import subprocess
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
import matplotlib.ticker as ticker
import os
import base64
from PIL import Image


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

                if indicador[1] == 'Aumentar nota dos PPGs':
                    # 1- Consulta: Obter notas dos alunos no programa específico
                    cur.execute("SELECT nota,quadrienal FROM resultadoavaliacao WHERE codigoprograma = '32003013014P4' ORDER BY quadrienal")
                    resultados = cur.fetchall()

                                        # Extrair as notas e a quadrienal dos resultados
                    notas = []
                    quadrienais = []
                    for resultado in resultados:
                        try:
                            nota = float(resultado[0])
                            notas.append(nota)
                            quadrienal = resultado[1]
                            quadrienais.append(quadrienal)
                        except ValueError:
                            # Se não for possível converter para float, ignore esse valor
                            pass

                    # Plotar o histograma das notas e quadrienais
                    fig, ax = plt.subplots(figsize=(10, 6))  # Ajuste o tamanho da figura conforme necessário
                    hb = ax.hist2d(notas, quadrienais, bins=(20, len(set(quadrienais))), cmap='Blues')  # Ajuste o número de bins e a cor
                    ax.set_xlabel('Nota')
                    ax.set_ylabel('Quadrienal')
                    ax.set_title('Distribuição das Notas CAPES por Quadrienal')
                    ax.grid(True)

                    # Adicionar barra de cores
                    plt.colorbar(hb[3], ax=ax)

                    # Exibir o gráfico utilizando Streamlit
                    st.pyplot(fig)
                # segunda consulta
                    consulta_quesitos = "select * from avaliacaoprog_adm"
                    cur.execute(consulta_quesitos)
                    dados_quesitos = cur.fetchall()
                                        
                                        # Exibir o DataFrame no Streamlit
                    df_quesitos = pd.DataFrame(dados_quesitos, columns=['Quesitos', '2017', '2021'])
                    st.write(df_quesitos)
                                    
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

                  
                
            except psycopg2.Error as e:
                    st.error("Erro durante a execução da segunda consulta: {}".format(e))
            finally:
                    conn.close()  # Fechar conexão com o banco de dados após concluir todas as operações de consulta


  
         # Adicionar botão de cadastro para Indicador
    if st.sidebar.button("Cadastrar Ação"):
       
        # Adicione aqui a lógica para cadastrar um novo Indicador no banco de dados
        #subprocess.run(["streamlit", "run", "c:/Users/thatt/Documents/Projeto_Streamlit/src/kanbam_adm.py"])

       
        def adicionar_tarefa():
            nova_tarefa = entrada.get()

            if nova_tarefa:
                lista_a_fazer.insert(tk.END, nova_tarefa)
                entrada.delete(0, tk.END)
            else:
                messagebox.showwarning("Aviso", "Digite uma tarefa válida!")

        def mover_para_em_andamento():
            try:
                selecionada = lista_a_fazer.curselection()[0]
                tarefa = lista_a_fazer.get(selecionada)
                lista_a_fazer.delete(selecionada)
                lista_em_andamento.insert(tk.END, tarefa)
            except IndexError:
                messagebox.showwarning("Aviso", "Selecione uma tarefa para mover para 'Em andamento'!")

        def mover_para_concluido():
            try:
                selecionada = lista_em_andamento.curselection()[0]
                tarefa = lista_em_andamento.get(selecionada)
                lista_em_andamento.delete(selecionada)
                lista_concluido.insert(tk.END, tarefa)
            except IndexError:
                messagebox.showwarning("Aviso", "Selecione uma tarefa para mover para 'Concluído'!")

        def remover_tarefa():
            try:
                selecionada = lista_concluido.curselection()[0]
                lista_concluido.delete(selecionada)
            except IndexError:
                messagebox.showwarning("Aviso", "Selecione uma tarefa para remover!")


