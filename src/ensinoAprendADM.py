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
consulta_discentes_MP = """
    SELECT anosituacao, nivel, sexo, anomatricula, situacao, COUNT(*)
    FROM discente
    WHERE codigoprograma = '32003013014P4' AND nivel = 'Mestrado Profissional'
    GROUP BY anosituacao, nivel, sexo, anomatricula, situacao
"""
dados_discentes = executar_consulta(consulta_discentes_MP)

# Consultar dsicentes Mestardo Profissional
consulta_discentes_MP = """
    SELECT anosituacao,anocoleta, nivel, sexo, anomatricula, situacao, COUNT(*)
    FROM discente
    WHERE codigoprograma = '32003013014P4' AND nivel = 'Mestrado Profissional'
    GROUP BY anosituacao,anocoleta, nivel, sexo, anomatricula, situacao
"""

dados_discentes_MP = executar_consulta(consulta_discentes_MP)

# Converter os resultados em um DataFrame do Pandas
df_discentes = pd.DataFrame(dados_discentes, columns=['anosituacao','anocoleta','nivel', 'sexo', 'anomatricula', 'situacao'])

# Função para consultar docentes no banco de dados
consulta_docentes = """ SELECT count (*), anocoleta FROM docente  WHERE codigoprograma = '32003013014P4' GROUP BY anocoleta"""
dados_docente = executar_consulta(consulta_docentes)

# Converter os resultados em um DataFrame do Pandas
df_docente = pd.DataFrame(dados_docente, columns=['anocoleta'])

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

   # Verifique se a métrica selecionada possui objetivos
   if metrica_selecionada == "Proporção aluno-funcionário":
      # Realiza cálculo 
      if ((df_discentes['nivel'] == 'Graduacao') & (df_discentes['situacao'] != 'DESLIGADO')):
        contg = dados_discentes
      
      if ((df_discentes['nivel']) == 'Mestrado Profissional' & (df_discentes['situacao'] != 'DESLIGADO')):
        contm= dados_discentes_MP
      
      count = df_docente[(df_docente)]
      resultado = contm + (contg * 0.5) / count
      st.write(f"Resultado da métrica:  {resultado}")

   # Verifique se a métrica selecionada possui objetivos
   elif metrica_selecionada == "Mestrado Pontual":
      # Realiza cálculo 
      contTC = len(df_discentes[(df_discentes['anosituacao']) & (df_discentes['situacao'] == 'TITULADO')])
      contMA = len(df_discentes[(df_discentes['anosituacao'] == ano_selecionado) & (df_discentes['situacao'] == 'TITULADO') & (df_discentes['anomatricula'] < ano_selecionado-2)])
      if contMA != 0:
         resultado = (contTC / contMA) * 100
      else:
         resultado = "Divisão por zero"
      st.write(f"Resultado da métrica: '{metrica_selecionada}' para o ano {ano_selecionado}: {resultado}")

   # Verifique se a métrica selecionada possui objetivos
   elif metrica_selecionada == "Pessoal acadêmico com doutoramento":
      # Realiza cálculo 
      contD = len(df_docente[(df_docente['anocoleta'] == ano_selecionado) & (df_docente['docente'] == 'Sim')])
      contM = len(df_docente[(df_docente['anocoleta'] == ano_selecionado)])
      if contM != 0:
         resultado = (contD / contM) * 100
      else:
         resultado = "Divisão por zero"
      st.write(f"Resultado da métrica: '{metrica_selecionada}' para o ano {ano_selecionado}: {resultado}")

   # Verifique se a métrica selecionada possui objetivos
   elif metrica_selecionada == "Contato com ambiente de trabalho (mestrado)":
      # Realiza cálculo 
      contAT = len(df_discentes[(df_discentes['anocoleta'] == ano_selecionado) & (df_discentes['nivel'] == 'Mestrado Profissional') & (df_discentes['situacao'] != 'DESLIGADO')])
      contTM = len(df_discentes[(df_discentes['anocoleta'] == ano_selecionado) & (df_discentes['nivel'] == 'Mestrado Profissional')])
      if contTM != 0:
         resultado = (contAT / contTM) * 100
      else:
         resultado = "Divisão por zero"
      st.write(f"Resultado da métrica: '{metrica_selecionada}' para o ano {ano_selecionado}: {resultado}")

   # Verifique se a métrica selecionada possui objetivos
   elif metrica_selecionada == "Equilíbrio de gênero":
      # Realiza cálculo 
      contF = len(df_discentes[(df_discentes['anocoleta'] == ano_selecionado) & (df_discentes['nivel'] == 'Mestrado Profissional') & (df_discentes['sexo'] == 'Feminino') & (df_discentes['situacao'] != 'DESLIGADO')])
      contM = len(df_discentes[(df_discentes['anocoleta'] == ano_selecionado) & (df_discentes['nivel'] == 'Mestrado Profissional') & (df_discentes['sexo'] == 'Masculino') & (df_discentes['situacao'] != 'DESLIGADO')])
      if contF != 0 and contM != 0:
         resultado = min(contF, contM) / max(contF, contM)
      else:
         resultado = "Divisão por zero"
      st.write(f"Resultado da métrica: '{metrica_selecionada}' para o ano {ano_selecionado}: {resultado}")

   else:
      st.write(f"Resultado da métrica: '{metrica_selecionada}' para o ano {ano_selecionado}: Em desenvolvimento")

# Exemplo de métricas e objetivos
if st.sidebar.checkbox("Exibir Métricas e Objetivos"):
   st.subheader("Métricas e Objetivos")
   st.write(dimensoes)