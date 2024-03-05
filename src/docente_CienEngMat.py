import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import psycopg2
import matplotlib
import seaborn as sns
import sys
# Desativa o aviso sobre o uso do Pyplot Global
st.set_option('deprecation.showPyplotGlobalUse', False)

matplotlib.use('Agg')


from utils.conect import conectar, fechar_conexao

# Função para conectar ao banco de dados
def executar_consulta(query):
    conn, cursor = conectar()
    try:
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        fechar_conexao(conn, cursor)

# Atualizar a função fechar_conexao para aceitar o cursor como argumento
def fechar_conexao(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()

# Consulta para obter dados da tabela docente
consulta_docente = """
SELECT DISTINCT ON (d.nome) sexo, nacionalidade, nivel, categoria, regimetrabalho
FROM docente d
WHERE codigoprograma = '32003013005P5' 
ORDER BY d.nome;
"""
dados_docente = executar_consulta(consulta_docente)

# Consulta para contar a quantidade de docentes por categoria
consulta_soma_categoria = "SELECT categoria,COUNT(DISTINCT nome) as soma_categoria FROM docente WHERE codigoprograma = '32003013005P5' GROUP BY categoria;"
dados_soma_categoria = executar_consulta(consulta_soma_categoria)

# Consulta para contar a quantidade de docentes orientador
consulta_soma_orientador = """SELECT orientador, COUNT(DISTINCT nome) AS quantidade, STRING_AGG(DISTINCT nome, '<br>') AS discentes FROM discente WHERE codigoprograma = '32003013005P5' AND orientador != ''
    GROUP BY orientador;"""
dados_soma_orientador = executar_consulta(consulta_soma_orientador)

# Criação de um DataFrame a partir dos resultados da segunda consulta
df_docente_soma_categoria = pd.DataFrame(dados_soma_categoria, columns=['categoria', 'soma_categoria'])

# Criação de um DataFrame a partir dos resultados da terceira consulta
df_discente_soma_orientador = pd.DataFrame(dados_soma_orientador, columns=['orientador', 'nome', 'soma_orientador'])

# ...

# Consulta producao intelectual docente
consulta_nome_docente_producao = """
    SELECT DISTINCT ON (p.autor) p.autor, p.tipoproducao, p.subtipo, p.anaopublicacao, p.titulo, d.nome AS nome_docente
    FROM producaointelectual p
    INNER JOIN docente d ON p.autor = d.nome
    WHERE p.codigoprograma = '32003013005P5' 
    ORDER BY p.autor, p.titulo;
"""

dados_producao = executar_consulta(consulta_nome_docente_producao )

# Aplicação Streamlit
st.title('Análise de Dados - Docentes')
st.sidebar.title('Opções')

# Mostrar tabela de dados da primeira consulta
if st.sidebar.checkbox('Mostrar dados de Docentes'):
    st.dataframe(pd.DataFrame(dados_docente, columns=[
        'sexo','nacionalidade','nivel','categoria','regimetrabalho']))

# Criar um gráfico de barras para a segunda consulta
if st.sidebar.checkbox('Gráfico de Barras de Categoria'):
    fig, ax = plt.subplots()
    ax.bar(df_docente_soma_categoria['categoria'], df_docente_soma_categoria['soma_categoria'])
    ax.set_xlabel('Categoria')
    ax.set_ylabel('Soma da Categoria')
    ax.set_title('Soma da Categoria por Categoria')
    st.pyplot(fig)

# Criação do gráfico de barras
if st.sidebar.checkbox('Gráfico de Orientador'):
    if not df_discente_soma_orientador.empty:
        try:
            # Agrupar por orientador e calcular a soma de alunos
            df_soma_alunos_por_orientador = df_discente_soma_orientador.groupby('orientador')['soma_orientador'].sum().reset_index()

            # Criação do gráfico interativo usando plotly express
            fig = px.bar(df_soma_alunos_por_orientador,
                         x='orientador',
                         y='soma_orientador',
                         title='Soma de Alunos por Orientador',
                         labels={'soma_orientador': 'Número de Alunos'},
                         height=500)

            # Adicionar interatividade
            fig.update_layout(hovermode='x unified')

            # Exibir o gráfico
            st.plotly_chart(fig)
        except Exception as e:
            st.warning(f'Erro ao criar gráfico: {e}')
    else:
        st.warning('Não há dados de discente para o código do programa especificado.')


if st.sidebar.checkbox('Mostrar dados Produção docente'):
    # Converter os resultados da consulta para um DataFrame do pandas
# Converter os resultados da consulta para um DataFrame do pandas
    df_producao = pd.DataFrame(dados_producao, columns=['autor', 'tipoproducao', 'subtipo', 'ano', 'titulo', 'nome_docente'])
    # Exibir o DataFrame
    st.dataframe(df_producao)

    # Criar o gráfico de dispersão com Plotly Express
    fig = px.scatter(df_producao, x='ano', y='autor', color='nome_docente', hover_data=['titulo'],
                     title='Produção Intelectual por Docente ao longo dos Anos',
                     labels={'ano': 'Ano', 'autor': 'Autor', 'nome_docente': 'Nome do Docente'})

    # Adicionar título e rótulos dos eixos
    fig.update_layout(title_x=0.5)

    # Exibir o gráfico
    st.plotly_chart(fig)


if st.sidebar.checkbox('Nivel'):
     # Execute a consulta SQL para extrair os dados da tabela docente
    consulta_docente1 = """
       SELECT nivel, sexo, COUNT(DISTINCT nome) AS num_docentes
        FROM docente 
        WHERE codigoprograma = '32003013005P5'
        GROUP BY nivel, sexo;
    """

     # Executar a consulta e obter os dados
    dados_docente1 = executar_consulta(consulta_docente1)

    # Criar um DataFrame pandas com os resultados
    df1 = pd.DataFrame(dados_docente1, columns=['nivel', 'sexo', 'count'])

    # Converter a coluna 'count' para tipo numérico
    df1['count'] = pd.to_numeric(df1['count'])

    # Verificar os dados retornados pela consulta
    st.write(df1)

    # Criar gráfico de barras empilhadas para comparar gênero por nível de ensino
    df_pivot = df1.pivot(index='nivel', columns='sexo', values='count')
    df_pivot.plot(kind='bar', stacked=True)
    plt.title('Distribuição de Gênero por Nível de Ensino')
    plt.xlabel('Nível de Ensino')
    plt.ylabel('Contagem')
    st.pyplot()  # Mostrar o gráfico no Streamlit

if st.sidebar.checkbox('Estrato qualis'):
 consulta_extrato= """
    SELECT DISTINCT q.titulo, q.estrato, d.nome AS nome_docente
    FROM qualis q
    INNER JOIN producaointelectual p ON q.titulo = p.titulo
    INNER JOIN docente d ON p.autor = d.nome
    WHERE q.nomeprograma = 'ENGENHARIAS II';
""" 
    # Executar a consulta e obter os dados
 dados_extrato = executar_consulta(consulta_extrato)

        # Criar um DataFrame pandas com os resultados
 df_extrato = pd.DataFrame(dados_extrato, columns=['Titulo', 'Estrato', 'Docente'])

 # Verificar os dados retornados pela consulta
 st.write(df_extrato)


if st.sidebar.checkbox('Periodicos'):
    # Consulta SQL para selecionar todos os dados da tabela 'periodicos'
    consulta_sql = "SELECT * FROM periodicos where codigoprograma ='32003013005P5;"

        # Executar a consulta e armazenar os resultados em um DataFrame
    dados_periodicos = executar_consulta(consulta_sql)
    df_periodicos = pd.DataFrame(dados_periodicos, columns=['Nome', 'H index Scopus', 'Citação Scopus','Publ Scopus','H index Web','Publ Web','Citação Web','Programa'])

    if dados_producao:
            # Transformar os dados em um DataFrame
            df_periodicos = pd.DataFrame(dados_periodicos, columns=['Nome', 'H index Scopus', 'Citação Scopus','Publ Scopus','H index Web','Publ Web','Citação Web','Programa'])

            # Exibir o DataFrame
            st.write(df_periodicos)

            # Gerar um gráfico de barras comparando os h-indexes do Scopus e do Web para cada docente
            plt.figure(figsize=(10, 6))
            sns.barplot(data=df_periodicos, x='Nome', y='H index Scopus', color='blue', label='H index Scopus')
            sns.barplot(data=df_periodicos, x='Nome', y='H index Web', color='red', label='H index Web')
            plt.xlabel('Nome do Docente')
            plt.ylabel('H-index')
            plt.title('Comparação do h-index do Scopus e do Web por Docente')
            plt.xticks(rotation=45, ha='right')
            plt.legend()
            st.pyplot()
    else:
            st.write("Nenhum dado retornado pela consulta SQL.")