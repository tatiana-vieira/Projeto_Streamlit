import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils.conect import conectar, fechar_conexao

# Set the backend for matplotlib
plt.switch_backend('Agg')

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
consulta_capes = """
SELECT sigla, quadrienal, nota FROM resultadoavaliacao where area_avaliacao = 'ADMINISTRAÇÃO PÚBLICA E DE EMPRESAS, CIÊNCIAS CONTÁBEIS E TURISMO'
"""
dados_capes = executar_consulta(consulta_capes)

# Transformar os resultados em DataFrame
df = pd.DataFrame(dados_capes, columns=['Sigla', 'Quadrienal', 'Nota'])

# Convert 'Nota' column to numeric, coercing errors to NaN
df['Nota'] = pd.to_numeric(df['Nota'], errors='coerce')

# Remove rows with NaN values in the 'Nota' column
df.dropna(subset=['Nota'], inplace=True)

# Get unique values of 'Sigla'
siglas = df['Sigla'].unique()

# Plotting each group of 'Sigla'
for sigla in siglas:
    # Filter data for the current 'Sigla'
    df_sigla = df[df['Sigla'] == sigla]
    
    # Pivot the DataFrame
    pivot_df = df_sigla.pivot_table(index='Quadrienal', values='Nota', aggfunc='mean')
    
    # Creating the plot
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df_sigla, x='Quadrienal', y='Nota', color='skyblue')
    plt.title(f'Nota por Quadrienal para {sigla}')
    plt.xlabel('Quadrienal')
    plt.ylabel('Nota')
    plt.xticks(rotation=45)
    
    # Exibir o gráfico com Streamlit
    st.pyplot()
    
    # Close the current figure to prevent memory leakage
    plt.close()