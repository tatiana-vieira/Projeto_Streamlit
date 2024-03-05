import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import psycopg2
import seaborn as sns

# Desativa o aviso sobre o uso do Pyplot Global
st.set_option('deprecation.showPyplotGlobalUse', False)

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

# Função para consultar discentes no banco de dados
consulta_discentes = """
    SELECT DISTINCT nome, orientador,datamatricula
    FROM discente
    WHERE codigoprograma = '32003013014P4'
    ORDER BY orientador ASC"""

dados_discentes = executar_consulta(consulta_discentes)

# Converter os resultados da consulta para um DataFrame do pandas
df_discentes = pd.DataFrame(dados_discentes, columns=['nome', 'orientador', 'datamatricula'])

# Aplicação Streamlit
st.title('Análise de Dados - Discentes')
st.sidebar.title('Opções')

# Mostrar tabela de dados dos discentes
if st.sidebar.checkbox('Mostrar dados dos Discentes'):
    st.dataframe(df_discentes)

# Criar um gráfico de barras para a quantidade de discentes por orientador
if st.sidebar.checkbox('Quantidade de Discentes por Orientador'):
    df_quantidade_discentes_por_orientador = df_discentes.groupby('orientador').size().reset_index(name='quantidade')
    fig = px.bar(df_quantidade_discentes_por_orientador, x='orientador', y='quantidade', title='Quantidade de Discentes por Orientador')
    st.plotly_chart(fig)

# Consulta para obter os alunos titulados por ano
consulta_alunos_titulados_por_ano = """
    SELECT anosituacao, COUNT(DISTINCT nome) AS quantidade_titulados
    FROM discente
    WHERE situacao = 'TITULADO' AND codigoprograma = '32003013014P4'
    GROUP BY anosituacao;
    """
dados_consulta_alunos_titulados_por_ano=executar_consulta(consulta_alunos_titulados_por_ano)

# Consulta para obter os alunos que têm bolsa e o nome da bolsa
consulta_alunos_com_bolsa = """
   SELECT DISTINCT nome, tipobolsa
FROM discente
WHERE (tipobolsa IS NOT NULL AND TRIM(tipobolsa) <> '') AND codigoprograma = '32003013014P4';
"""
dados_consulta_alunos_com_bolsa=executar_consulta(consulta_alunos_com_bolsa)

# Consulta para obter os alunos e seus orientadores
consulta_alunos_orientadores = """
    SELECT orientador, COUNT(DISTINCT nome) AS quantidade, STRING_AGG(DISTINCT nome, '<br>') AS discentes
    FROM discente
    WHERE codigoprograma = '32003013014P4' AND orientador != ''
    GROUP BY orientador;
"""

dados_consulta_alunos_orientadores =executar_consulta(consulta_alunos_orientadores)

#consulta sexo
consulta_alunos_sexo =""" SELECT sexo, COUNT(DISTINCT nome) AS quantidade_discentes
FROM discente where codigoprograma = '32003013014P4'
GROUP BY sexo;"""

dados_Sexo = executar_consulta(consulta_alunos_sexo)

#Consulta producao relevante por ano
consulta_prodrelevante = """    
 select ano,autor,categoria,titulo from prodrelevante where codigoprograma = '32003013014P4' and categoria = 'Discente' order by ano"""

dados_consulta_prodrelevante =executar_consulta(consulta_prodrelevante)

# Verificar se a opção 'Alunos Titulados por Ano' foi selecionada
if st.sidebar.checkbox('Alunos Titulados por Ano'):
    # Transformar os resultados da consulta em um DataFrame pandas
    df_alunos_titulados_por_ano = pd.DataFrame(dados_consulta_alunos_titulados_por_ano, columns=['ano', 'quantidade_titulados'])

    # Criar um gráfico de barras agrupadas com Plotly
    fig = px.bar(df_alunos_titulados_por_ano, x='ano', y='quantidade_titulados',
                labels={'quantidade_titulados': 'Quantidade de Alunos Titulados', 'ano': 'Ano'},
                title='Quantidade de Alunos Titulados por Ano',
                color_discrete_sequence=px.colors.qualitative.Plotly)
    fig.update_layout(xaxis_type='category', xaxis={'categoryorder': 'total ascending'})
    fig.show()
    

# Verificar se a opção 'Alunos com Bolsa' foi selecionada
if st.sidebar.checkbox('Alunos com Bolsa'):
    # Transformar os resultados da consulta em um DataFrame pandas
    df_alunos_com_bolsa = pd.DataFrame(dados_consulta_alunos_com_bolsa, columns=['nome', 'tipobolsa'])

    # Contar a frequência de cada tipo de bolsa
    df_counts = df_alunos_com_bolsa['tipobolsa'].value_counts().reset_index()
    df_counts.columns = ['tipobolsa', 'quantidade']

    # Criar um gráfico de barras empilhadas com Seaborn
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df_counts, x='quantidade', y='tipobolsa', palette=sns.color_palette("viridis", n_colors=len(df_counts)))
    plt.title('Distribuição de Tipos de Bolsa entre Alunos')
    plt.xlabel('Quantidade de Alunos')
    plt.ylabel('Tipo de Bolsa')
    plt.grid(True, axis='x')
    st.pyplot()  # Mostrar 

# Verificar se a opção 'Alunos e Seus Orientadores' foi selecionada
if st.sidebar.checkbox('Alunos e Seus Orientadores'):
    # Transformar os resultados da consulta em um DataFrame pandas
    # Converter os dados para DataFrame
    df_alunos_orientadores = pd.DataFrame(dados_consulta_alunos_orientadores, columns=['Orientador', 'Quantidade', 'Discentes'])

    # Criar gráfico de barras com Plotly Express
    fig1 = px.bar(df_alunos_orientadores, x='Quantidade', y='Orientador', orientation='h', text='Discentes',
                  title='Quantidade de Alunos por Orientador',
                  labels={'Quantidade': 'Quantidade de Alunos', 'Orientador': 'Orientador'})

    # Exibir gráfico usando st.plotly_chart()
    st.plotly_chart(fig1)

if st.sidebar.checkbox('Alunos - Masculino e Feminino)'):
     # Conversão dos dados para DataFrame
    df_sexo = pd.DataFrame(dados_Sexo, columns=['Sexo', 'Quantidade de Discentes'])

    # Configurações do gráfico
    fig, ax = plt.subplots()
    ax.bar(df_sexo['Sexo'], df_sexo['Quantidade de Discentes'], color=['pink', 'blue'])

    # Adicionando título e rótulos dos eixos
    ax.set_title('Quantidade de Discentes por Sexo')
    ax.set_xlabel('Sexo')
    ax.set_ylabel('Quantidade de Discentes')

    # Exibir o gráfico
    st.pyplot(fig)
if st.sidebar.checkbox('Produção Relevante'):
    # Executar a consulta

    # Criar um DataFrame com os dados
    df = pd.DataFrame(dados_consulta_prodrelevante, columns=['Ano', 'Autor', 'Categoria', 'Título'])

    # Mostrar os dados em um quadro
    st.write("Dados da Consulta:")
    st.write(df)

    # Mostrar os dados em um gráfico de barras por ano
    contagem_por_ano = df['Ano'].value_counts().sort_index()
    plt.bar(contagem_por_ano.index, contagem_por_ano.values)
    plt.xlabel('Ano')
    plt.ylabel('Número de Produções Relevantes')
    plt.title('Produções Relevantes por Ano')
    st.pyplot(plt)