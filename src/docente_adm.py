import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import psycopg2

from utils.conect import conectar, fechar_conexao

# Função para conectar ao banco de dados
def executar_consulta(query):
    conn = conectar()
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        fechar_conexao(conn)

# Consulta para obter dados da tabela docente
consulta_docente = "SELECT * FROM docente where codigoprograma = '32003013014P4';"
dados_docente = executar_consulta(consulta_docente)

# Consulta para contar a quantidade de docentes por categoria
consulta_soma_categoria = "SELECT categoria, COUNT(*) as soma_categoria FROM docente WHERE codigoprograma = '32003013014P4' GROUP BY categoria;"
dados_soma_categoria = executar_consulta(consulta_soma_categoria)

# Consulta para contar a quantidade de docentes orientador
consulta_soma_orientador = "SELECT orientador, nome, COUNT(*) as soma_orientador FROM discente WHERE codigoprograma ='32003013014P4' GROUP BY orientador, nome;"
dados_soma_orientador = executar_consulta(consulta_soma_orientador)


# Criação de um DataFrame a partir dos resultados da segunda consulta
df_docente_soma_categoria = pd.DataFrame(dados_soma_categoria, columns=['categoria', 'soma_categoria'])

# Criação de um DataFrame a partir dos resultados da terceira consulta
df_discente_soma_orientador = pd.DataFrame(dados_soma_orientador, columns=['orientador', 'nome', 'soma_orientador'])

# ...

# Aplicação Streamlit
st.title('Análise de Dados - Docentes')
st.sidebar.title('Opções')

# Mostrar tabela de dados da primeira consulta
if st.sidebar.checkbox('Mostrar dados da tabela Docente'):
    st.dataframe(pd.DataFrame(dados_docente, columns=[
        'nome', 'nacionalidade', 'email', 'nivel', 'anaotitulacao', 'areconhecimento',
        'paisinstituicao', 'instituicao', 'tipovinculo', 'categoria', 'cargahoraria',
        'inicio', 'fim', 'mestradoacademico', 'mestradoprofissional', 'doutorado',
        'doutoradoprofissional', 'tutoria', 'monografia', 'iniciacaocinetifica',
        'disciplinagraducao', 'cargahorariaanual', 'motivoafastamento',
        'datainicioafast', 'datafimafast', 'instituicaoensinoafast', 'anocoleta',
        'codigoprograma'
    ]))

# Mostrar tabela de dados da segunda consulta
if st.sidebar.checkbox('Mostrar dados da tabela Soma Categoria'):
    st.dataframe(df_docente_soma_categoria)



# Criar um gráfico de barras para a segunda consulta
if st.sidebar.checkbox('Gráfico de Barras - Soma da Categoria por Categoria'):
    fig, ax = plt.subplots()
    ax.bar(df_docente_soma_categoria['categoria'], df_docente_soma_categoria['soma_categoria'])
    ax.set_xlabel('Categoria')
    ax.set_ylabel('Soma da Categoria')
    ax.set_title('Soma da Categoria por Categoria')
    st.pyplot(fig)



# Criação do gráfico de barras
# Criação do gráfico de barras
# Criação do gráfico de barras
if st.sidebar.checkbox('Gráfico Interativo - Orientador'):
    if not df_discente_soma_orientador.empty:
        try:
            # Agrupar por orientador e calcular a soma de alunos
            df_soma_alunos_por_orientador = df_discente_soma_orientador.groupby(['orientador', 'nome'])['soma_orientador'].sum().reset_index()

            # Criação do gráfico interativo usando plotly express
            fig = px.bar(df_soma_alunos_por_orientador,
                         x='orientador',
                         y='soma_orientador',
                         color='nome',  # Usar color para representar cada aluno
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