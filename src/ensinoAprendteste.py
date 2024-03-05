import streamlit as st
import pandas as pd
from utils.conect import conectar, fechar_conexao

# Inicialize as variáveis
contg = 0
contm = 0
count = 0

# Exemplo de uso
conn = conectar()

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

# Consultas tabelas
# Função para consultar discentes no banco de dados
# Consultar discentes Mestrado Profissional
consulta_discentes_MP = """
    SELECT COUNT(DISTINCT nome) AS count_unique_discente, anosituacao, nivel, sexo, anomatricula, situacao
    FROM discente
    WHERE codigoprograma = '32003013014P4' AND nivel = 'Mestrado Profissional' and situacao != 'DESLIGADO'
    GROUP BY anosituacao, nivel, sexo, anomatricula, situacao
"""

dados_discentes_MP = executar_consulta(consulta_discentes_MP)

# Consultar dsicentes Mestrado Profissional
consulta_discentes = """
    SELECT COUNT(DISTINCT nome) AS count_unique_discente, anosituacao, nivel, sexo, anomatricula, situacao
    FROM discente
    WHERE codigoprograma = '32003013014P4' AND nivel = 'Graduação' and situacao != 'DESLIGADO'
    GROUP BY anosituacao, nivel, sexo, anomatricula, situacao
"""

dados_discentes = executar_consulta(consulta_discentes)

# Converter os resultados em um DataFrame do Pandas
df_discentes = pd.DataFrame(dados_discentes, columns=['anosituacao', 'nivel', 'sexo', 'anomatricula', 'situacao'])

# Função para consultar docentes no banco de dados
consulta_docentes = """ SELECT count (Distinct nome) AS count_unique_docentes FROM docente WHERE codigoprograma = '32003013014P4' """

dados_docente = executar_consulta(consulta_docentes)

# Converter os resultados em um DataFrame do Pandas
df_docente = pd.DataFrame(dados_docente)

# Dicionário de dimensões, métricas e objetivos
dimensoes = {
    "Ensino e Aprendizagem": {
       "metricas": [
            "Proporção aluno-funcionário",
            "Mestrado Pontual",
            "Pessoal acadêmico com doutoramento",
            "Contato com ambiente de trabalho (mestrado)",
            "Equilíbrio de gênero"
        ],
        "objetivos": {
            "Proporção aluno-funcionário": ["Reduzir a proporção para melhorar o atendimento individual", "Manter uma proporção equilibrada"],
            "Mestrado Pontual": ["Aumentar a taxa de graduação", "Fornecer suporte adicional aos estudantes"],
            "Pessoal acadêmico com doutoramento": ["Aumentar o número de professores com doutorado", "Garantir que 70% do pessoal tenha doutorado"],
            "Contato com ambiente de trabalho (mestrado)": ["Aumentar o número de estudantes com experiência de trabalho", "Melhorar a qualidade das experiências"],
            "Equilíbrio de gênero": ["Alcançar equilíbrio de gênero de 50/50", "Promover a igualdade de gênero"]
        }
    },
}

# Título da página
st.markdown("<h1 style='text-align: center; font-size: 24px;'>Mestrado Profissional - Administração</h1>", unsafe_allow_html=True)

# Layout em uma única coluna (canto esquerdo)
st.sidebar.title("Selecione as Opções")

# Seleção do Ano
#ano_selecionado = st.sidebar.selectbox("Selecione o Ano", [2020, 2021, 2022, 2023, 2024])

# Seleção da Dimensão
dimensao_selecionada = st.sidebar.selectbox("Selecione a Dimensão", list(dimensoes.keys()))

# Seleção da Métrica
metrica_selecionada = st.sidebar.selectbox("Selecione a Métrica", dimensoes[dimensao_selecionada]["metricas"])

# Botão para gerar resultados
if st.sidebar.button("Gerar Resultados"):
   #st.write("Ano selecionado:", ano_selecionado)
   st.write("Dimensão selecionada:", dimensao_selecionada)
   st.write("Métrica selecionada:", metrica_selecionada)

if metrica_selecionada == "Proporção aluno-funcionário":
    contg = dados_discentes      
    contm = dados_discentes_MP      
    count = dados_docente
st.write(count)
    # Verifique se count não é zero antes de fazer a divisão
# Verificar se count não é zero antes de fazer a divisão
# Verificar se count não é zero antes de fazer a divisão
# Verificar se count não é zero antes de fazer a divisão
if count != 0:
    # Verificar se contm e contg são listas ou DataFrames
    if isinstance(contm, (list, pd.DataFrame)) and isinstance(contg, (list, pd.DataFrame)):
        # Calcular a soma de contm e contg corretamente
        if contm:
            if isinstance(contm[0], tuple):
                contm = sum([x[0] for x in contm])
            else:
                contm = sum(contm)
        
        if contg:
            if isinstance(contg[0], tuple):
                contg = sum([x[0] for x in contg])
            else:
                contg = sum(contg)
        
        # Verificar se contg e count são valores numéricos antes de fazer a multiplicação
        if isinstance(contg, (int, float)) and isinstance(count, (int, float)):
            # Realizar a soma e a divisão corretamente
            resultado = contm + (contg * 0.5) / count
            st.write(f"Resultado da métrica:  {resultado}")
        else:
            st.write("Os contadores contg e count devem ser valores numéricos.")
    else:
        st.write("Os contadores contm e contg devem ser listas ou DataFrames.")
else:
    st.write("Não há dados disponíveis para calcular a métrica de docentes. Impossível calcular a métrica.")