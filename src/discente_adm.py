import psycopg2
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

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
query = "SELECT * FROM discente WHERE codigoprograma = '32003013014P4';"
dados_discente = executar_consulta(query)


# Consulta para contar a quantidade de docentes orientador
consulta_soma_orientador = "SELECT orientador, nome, COUNT(*) as soma_orientador FROM discente WHERE codigoprograma ='32003013014P4' GROUP BY orientador, nome;"
dados_soma_orientador = executar_consulta(consulta_soma_orientador)


# Criação de um DataFrame a partir dos resultados da terceira consulta
df_discente_soma_orientador = pd.DataFrame(dados_soma_orientador, columns=['orientador', 'nome', 'soma_orientador'])

# ...

# Aplicação Streamlit
st.title('Análise de Dados - Discentes')
st.sidebar.title('Opções')

# Mostrar tabela de dados da primeira consulta
if st.sidebar.checkbox('Mostrar dados da tabela Discente'):
    st.dataframe(pd.DataFrame(dados_discente, columns=[
        'nome','sexo', 'nacionalidade', 'email', 'nivel', 'curso','Ano Matricula','situacao', 'anosituacao',
        'datasituacao', 'Complementar Bolsa', 'Orientador', 'Periodo Orientação', 'Principal',
        'Tipo bolsa', 'financiador', 'Programa fomento', 'IES', 'Nivel Bolsa',
        'Ano Coleta', 'Programa', 'Data Matricula'  ]))


# Criação do gráfico de barras
if st.sidebar.checkbox('Gráfico Interativo - Orientador'):
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


