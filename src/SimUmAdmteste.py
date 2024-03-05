import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


from utils.conect import conectar, fechar_conexao

# Função para executar consulta e retornar um DataFrame
def executar_consulta(query):
    conn, cursor = conectar()
    try:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        return pd.DataFrame(cursor.fetchall(), columns=columns)
    finally:
        fechar_conexao(conn, cursor)

# Atualizar a função fechar_conexao para aceitar o cursor como argumento
def fechar_conexao(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()
#########################################U-Multirank#########################################################################################
# Consulta para obter dados da tabela Ensino Aprendizado U_m
consulta_ensinoum = "SELECT nome, pais, mestradotempocerto, equilibriogenero, pessoalacaddoutorado, contatoambientetrabalho, proporcao FROM ensinoaprendiz1 WHERE programa = 'Administracao' OR programa = 'ADMINISTRACAO';"
cursor_ensinoum = executar_consulta(consulta_ensinoum)

# Consulta para obter dados da tabela Pesquisar
consulta_pesquisar = "SELECT * FROM pesquisar where programa = 'Administracao';"
cursor_pesquisar = executar_consulta(consulta_pesquisar)

# Consulta para obter dados da tabela Transferência de Conhecimento
consulta_transfconhecimento = "SELECT * FROM transfconhecimento where programa = 'Administracao';"
cursor_transfconhecimento = executar_consulta(consulta_transfconhecimento)

# Consulta para obter dados da tabela Orientação internacional
consulta_orientacaointern = "SELECT * FROM orientacaointern where programa = 'Administracao';"
cursor_orientacaointern = executar_consulta(consulta_orientacaointern)

# Consulta para obter dados da tabela engajamento regional
consulta_engajreg = "SELECT * FROM engajreg where programa = 'Administracao';"
cursor_engajreg = executar_consulta(consulta_engajreg)

###################################################CAPES########################################################################################
# Consulta para contar a quantidade de docentes por categoria
consulta_soma_categoria = "SELECT categoria,COUNT(DISTINCT nome) as soma_categoria FROM docente WHERE codigoprograma = '32003013014P4' GROUP BY categoria;"
dados_soma_categoria = executar_consulta(consulta_soma_categoria)

#Consulta perioso orientacao
consulta_orientacao = """SELECT COUNT(*) AS total_orientacoes
FROM (
    SELECT DISTINCT(NOME), ORIENTADOR, PERIODOORIENTACAO
    FROM DISCENTE
    WHERE CODIGOPROGRAMA = '32003013014P4'
        AND ORIENTADOR <> ''
) AS subquery
WHERE 
    SUBSTRING(PERIODOORIENTACAO, 7, 4)::int <= 2021;"""
cursor_orientacao = executar_consulta(consulta_orientacao)

consulta_andamento = """SELECT COUNT(*) AS total_orientacoes
FROM (
    SELECT DISTINCT(NOME), ORIENTADOR, PERIODOORIENTACAO
    FROM DISCENTE
    WHERE CODIGOPROGRAMA = '32003013014P4'
        AND ORIENTADOR <> ''
) AS subquery
WHERE 
    SUBSTRING(PERIODOORIENTACAO, 7, 4)::int > 2021;"""
dados_andamento = executar_consulta(consulta_andamento)


##tempo medio de titulação
# Consulta para calcular o tempo médio de titulação e o total de alunos titulados
consulta_media = """
SELECT AVG(anosituacao - anomatricula) AS tempo_medio_titulacao, COUNT(DISTINCT nome) AS total_titulados
FROM discente
WHERE situacao = 'TITULADO' AND codigoprograma = '32003013014P4';
"""
dados_consulta_alunos_titulados_por_ano = executar_consulta(consulta_media)

###################################################################################################################################################
 #Consulta para calcular o tempo médio de titulação e o total de alunos titulados
consulta_citacao_prodint = """
SELECT p.titulo, p.autor,p.categoria, c.citacaoscopus, c.citacaowebofscience
FROM producaointelectual AS p
JOIN citacao AS c ON p.titulo = c.titulo
WHERE (p.codigoprograma = '32003013014P4') and (p.categoria='Discente' or p.categoria='Egresso') and (c.citacaoscopus <> 0 or c.citacaowebofscience <> 0)
"""
dadosconsulta_citacao_prodint = executar_consulta(consulta_citacao_prodint)

 #Consulta para calcular o tempo médio de titulação e o total de alunos titulados
consulta_citacao_prodrel ="""SELECT p.titulo, p.autor,p.categoria, c.citacaoscopus, c.citacaowebofscience
FROM prodrelevante AS p
JOIN citacao AS c ON p.titulo = c.titulo
WHERE (p.codigoprograma = '32003013014P4') and (p.categoria='Discente' or p.categoria='Egresso') and (c.citacaoscopus <> 0 or c.citacaowebofscience <> 0)

 """
dadosconsulta_citacao_prodrel = executar_consulta(consulta_citacao_prodrel)


consulta_recursos = """
SELECT titulo,financiadores from CITACAO where codigoprograma = '32003013014P4' and financiadores <> '' ;
"""
dados_consulta_recursos = executar_consulta(consulta_recursos)

consulta_internacional = """
SELECT titulo,parceriaautinternacional from CITACAO where codigoprograma = '32003013014P4' and parceriaautinternacional <> ''
"""
dados_internacional = executar_consulta(consulta_internacional)

#####################################################################################################################################################

# Aplicação Streamlit
st.sidebar.title('Simulação Multidimensional')

opcao = st.sidebar.selectbox('Selecione uma opção:',['U-Multirank','CAPES'])

if opcao != 'Escolha uma opção':
    st.title(f'{opcao}')
   
if opcao == 'U-Multirank':
   opcao1 = st.sidebar.selectbox('Selecione uma opção:',['Ensino Aprendizagem', 'Pesquisa','Transferência de Conhecimento','Orientação Internacional','Engajamento Regional'])

   if opcao1 =='Ensino Aprendizagem':
       # Convertendo a coluna 'proporcao' para float
       st.write("Resultados da consulta:")
       st.dataframe(cursor_ensinoum)

   elif opcao1 == 'Pesquisa':
       st.subheader('Dados de Pesquisar')
       st.dataframe(cursor_pesquisar.fillna(0))  # Preenchendo os valores nulos com zero

   elif opcao1 == 'Transferência de Conhecimento':
       st.subheader('Dados de Transferência de Conhecimento')
       st.dataframe(cursor_transfconhecimento.fillna(0))  # Preenchendo os valores nulos com zero

   elif opcao1 == 'Orientação Internacional':
       st.subheader('Dados de Orientação Internacional')
       st.dataframe(cursor_orientacaointern.fillna(0))  # Preenchendo os valores nulos com zero 
 
   elif opcao1 == 'Engajamento Regional':
       st.subheader('Dados de Engajamento Regional')
       st.dataframe(cursor_engajreg.fillna(0))  # Preenchendo os valores nulos com zero
##################################################################################################################################################
elif opcao == 'CAPES':    
    opcao2 = st.sidebar.selectbox('Selecione uma opção:', ['Ensino e Aprendizagem', 'Pesquisa e Produção Científica', 'Internacionalização','Inovação e Transferência de Conhecimento','Impacto e Relevância da Sociedade'])

   #############docente permanente
    if opcao2 == 'Ensino e Aprendizagem':
        st.title('Alunos Titulados, abandonados e desligados')
        # Converter os resultados da consulta para um DataFrame pandas
        # Dados da consulta
        # Verificar os dados retornados
        st.write("Dados retornados pela consulta:")
        st.write(dados_soma_categoria)

        # Se os dados estiverem corretos, prosseguir com a criação do gráfico
        if not dados_soma_categoria.empty:
            # Configurar o gráfico
            plt.figure(figsize=(10, 6))
            plt.barh(dados_soma_categoria['categoria'], dados_soma_categoria['soma_categoria'], color='skyblue')
            plt.xlabel('Quantidade')
            plt.ylabel('Categoria')
            plt.title('Quantidade de Docentes por Categoria')
            plt.grid(axis='x', linestyle='--', alpha=0.7)  # Adiciona linhas de grade no eixo x
            plt.tight_layout()

            # Exibir o gráfico no Streamlit
            st.pyplot(plt)

        ####### Orientação concluida e andamento
        # Exibir os DataFrames com os resultados
        st.write("Orientações concluídas até 2021:")
        st.write(cursor_orientacao)

        st.write("\nOrientações em andamento após 2021:")
        st.write(dados_andamento)

        #################Extrair os resultados tempo medio titulado
        tempo_medio_titulacao, total_titulados = dados_consulta_alunos_titulados_por_ano.values[0]

        # Mostrar os resultados no Streamlit
        st.write("Tempo Médio de Titulação:", tempo_medio_titulacao)
        st.write("Total de Alunos Titulados:", total_titulados)
    #################################################################################################
    elif opcao2 =='Pesquisa e Produção Científica':
            st.title('Citacações Produções qualificadas alunos/egressos')

          
            # Criar visualizações com os dados
            st.title('Visualizações das Consultas')

            # Visualização 1: Tabela dos dados de citação
            st.subheader('Citações de Produção Intelectual')
            st.write(dadosconsulta_citacao_prodint)

            # Visualização 2: Tabela dos dados de citação
            st.subheader('Citações de Produções \relevantes')
            st.write(dadosconsulta_citacao_prodrel)


            # Visualização 2: Tabela dos dados de recursos
            st.subheader('Dados de Recursos')
            st.write(dados_consulta_recursos)          
 
#################################################################################################################################3
    elif opcao2 =='Internacionalização':
            st.title('Produções com autores internacionais')
    # Visualização 3: Tabela dos dados internacionais
            st.subheader('Dados Internacionais')
            st.write(dados_internacional)

###################################################################################################################################
    elif opcao2 =='Inovação e Transferência de Conhecimento':
            st.title('Produções/Patentes/Parcerias')



    elif opcao2 =='Impacto e Relevância da Sociedade':
            st.title('Egressos/Altmetrics')