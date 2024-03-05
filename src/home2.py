from PIL import Image
import streamlit as st
import os
import subprocess
from utils.conect import conectar, fechar_conexao
import pandas as pd

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

# Set a fixed width for buttons
button_width = 150

# Set a fixed size for images
image_width = 100

# Set a fixed size for text boxes
text_box_height = 100

# Carregando a imagem
image = Image.open('imagens\\PPG.png')
# Definindo o layout em duas colunas
col1, col2, col3, col4, col5, col6, col7, col8 = st.columns([1, 2, 3, 4, 1, 2, 3, 4])

# Primeira coluna: imagem centralizada
col4.image(image, use_column_width=50)

# Definindo o estilo CSS para o título
titulo_style = """
<style>
  h1 {
   text-align:center;
   color:#00498b; #cor azul escuro
  }
"""
st.markdown(titulo_style, unsafe_allow_html=True)

# Adicionando mais duas colunas
col1, col2, col3, col4 = st.columns(4)

programaselecionado = st.sidebar.selectbox('Selecione um programa de pós-graduação da UNIFEI : ',
                                         ['Escolha uma opção','Administração', 'Ciência e Engenharia de Materiais', 'Ciência e Tecnologia da Informação', 'Engenharia Elétrica', 'Engenharia de produção'])

# Exibir colunas e botões apenas quando um programa é selecionado
if programaselecionado != 'Escolha uma opção':
    st.title(f'Mestrado em {programaselecionado}')

    # Carregando a imagem docente
    image_docente = Image.open('imagens\\professor.png')
    # Carregando a imagem producao Relevante
    

    image_producaorelevante = Image.open('imagens\\ideia.png')
        # Carregando a imagem producao Relevante
    image_pdi = Image.open('imagens\\PDI3.png')
   
    # image_multirank_path = os.path.join('imagens', 'transferir.png')
    image_multirank_path = os.path.join('imagens', 'multi.png')
    image_multirank = Image.open(image_multirank_path)
   
    # Definindo o layout em duas colunas
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

    with col1:
        if st.button('Docente'):
            st.markdown(
                f'<button style="width: {button_width}px; height: {text_box_height}px">Docentes</button>',
                unsafe_allow_html=True
            )
            if programaselecionado == 'Administração':
                subprocess.run(["streamlit", "run", "c:/Users/thatt/Documents/Projeto_Streamlit/src/docente_adm.py"])
            elif programaselecionado == 'Ciência e Engenharia de Materiais':
                subprocess.run(["streamlit", "run", "c:/Users/thatt/Documents/Projeto_Streamlit/src/docente_CienEngMat.py"])
            # Add conditions for other programs as needed
        st.image(image_docente, width=image_width)
        st.markdown("&nbsp;", unsafe_allow_html=True)

    with col2:
        if st.button('Produção Relevante'):
            st.markdown(
                f'<button style="width: {button_width}px; height: {text_box_height}px">Produções Relevantes</button>',
                unsafe_allow_html=True
            )
            # Conteúdo específico para 'Produções Relevantes' no programa selecionado
            if programaselecionado == 'Administração':
                subprocess.run(["streamlit", "run", "c:/Users/thatt/Documents/Projeto_Streamlit/src/ProdRelevante_Adm.py"])
            elif programaselecionado == 'Ciência e Engenharia de Materiais':
                subprocess.run(["streamlit", "run", "c:/Users/thatt/Documents/Projeto_Streamlit/src/ProdrelevanteCienEngMat.py"])
                
            # Adicione condições para outros programas conforme necessário

        st.image(image_producaorelevante, width=image_width)
        st.markdown("&nbsp;", unsafe_allow_html=True)  # Adicionando espaço vertical

    with col3:
        if st.button('PDI'):
            st.markdown(
                f'<button style="width: {button_width}px; height: {text_box_height}px">PDI</button>',
                unsafe_allow_html=True
            )
            if programaselecionado == 'Administração':
                 subprocess.run(["streamlit","run", "c:/Users/thatt/Documents/Projeto_Streamlit/src/planoADMteste.py"])
            elif programaselecionado == 'Ciência e Engenharia de Materiais':
                subprocess.run(["streamlit","run", "c:/Users/thatt/Documents/Projeto_Streamlit/src/planoCienEngMat.py"])
          
        st.image(image_pdi, width=image_width)
        st.markdown("&nbsp;", unsafe_allow_html=True)  # Adicionando espaço vertical

    with col4:
        if st.button('Multidimensional'):
            st.markdown(
                f'<button style="width: {button_width}px; height: {text_box_height}px">Avaliação Multidimensional</button>',
                unsafe_allow_html=True
            )
            if programaselecionado == 'Administração':
                subprocess.run(["streamlit","run", "c:/Users/thatt/Documents/Projeto_Streamlit/src/SimUmAdmteste.py"])
            elif programaselecionado == 'Ciência e Engenharia de Materiais':
                st.write('Conteúdo específico para Simulações U-Multirank em Ciência e Engenharia de Materiais')
                subprocess.run(["streamlit","run", "c:/Users/thatt/Documents/Projeto_Streamlit/src/SimUmCienEngMat.py"])
            # Adicione condições para outros programas conforme necessário

        st.image(image_multirank, width=image_width)
        st.markdown("&nbsp;", unsafe_allow_html=True)  # Adicionando espaço vertical

    # Carregando as imagens de baixo
    image_discente = Image.open('imagens\\aluno.png')
    # Carregando a imagem producao Relevante
    image_engajamento = Image.open('imagens\\mundo.png')
    # Carregando a imagem producao Relevante
    image_comparar = Image.open('imagens\\comparar.png')
    # Carregando a imagem Planejamento Estrategico
    image_planejamento = Image.open('imagens\\planejestrategico.png')

    # Adicionar mais três imagens abaixo das anteriores
    col5, col6, col7, col8 = st.columns([1, 1, 1, 1])

    with col5:
        if st.button('Discente'):
            st.markdown(
                f'<button style="width: {button_width}px; height: {text_box_height}px">Discentes</button>',
                unsafe_allow_html=True
            )
            # Conteúdo específico para 'Discentes' no programa selecionado
            if programaselecionado == 'Administração':
                subprocess.run(["streamlit","run", "c:/Users/thatt/Documents/Projeto_Streamlit/src/discente_adm.py"])
            elif programaselecionado == 'Ciência e Engenharia de Materiais':
               subprocess.run(["streamlit","run", "c:/Users/thatt/Documents/Projeto_Streamlit/src/discente_CienEngMat.py"])
        st.image(image_discente, width=image_width)
        st.markdown("&nbsp;", unsafe_allow_html=True)  # Adicionando espaço vertical

    with col6:
        if st.button('Produção Intelectual'):
            st.markdown(
                f'<button style="width: {button_width}px; height: {text_box_height}px">Produção Intelectual</button>',
                unsafe_allow_html=True
            )
            if programaselecionado == 'Administração':
                st.write('Conteúdo específico para Discentes em Administração')
                subprocess.run(["streamlit","run", "c:/Users/thatt/Documents/Projeto_Streamlit/src/ProdCient_adm.py"])
            elif programaselecionado == 'Ciência e Engenharia de Materiais':
                subprocess.run(["streamlit","run", "c:/Users/thatt/Documents/Projeto_Streamlit/src/ProdCientCienEngMat.py"])
        st.image(image_engajamento, width=image_width)
        st.markdown("&nbsp;", unsafe_allow_html=True)  # Adicionando espaço vertical

    with col7:
        if st.button('Comparação'):
            st.markdown(
                f'<button style="width: {button_width}px; height: {text_box_height}px">Comparação</button>',
                unsafe_allow_html=True
            )
            if programaselecionado == 'Administração':
                subprocess.run(["streamlit","run", "c:/Users/thatt/Documents/Projeto_Streamlit/src/comparqualisAdm.py"])
            elif programaselecionado == 'Ciência e Engenharia de Materiais':
                st.write('Conteúdo específico para Discentes em Ciência')
        st.image(image_comparar, width=image_width)
        st.markdown("&nbsp;", unsafe_allow_html=True)  # Adicionando espaço vertical

    with col8:
        if st.button('Planejamento'):
            st.markdown(
                f'<button style="width: {button_width}px; height: {text_box_height}px">Planejamento Estratégico</button>',
                unsafe_allow_html=True
            )
            if programaselecionado == 'Administração':
                st.write('Conteúdo específico para Discentes em Administração')
                subprocess.run(["streamlit","run", "c:/Users/thatt/Documents/Projeto_Streamlit/src/Tarefas_Adm.py"])
            elif programaselecionado == 'Ciência e Engenharia de Materiais':
                st.write('Conteúdo específico para Discentes em Ciência')
        st.image(image_planejamento, width=image_width)
        st.markdown("&nbsp;", unsafe_allow_html=True)  # Adicionando espaço vertical

##################################################################################################################
capesselecionado = st.sidebar.selectbox('Selecione um programa da CAPES: ',
                                          ['Escolha uma opção','Administração', 'Ciência e Engenharia de Materiais', 'Ciência e Tecnologia da Informação', 'Engenharia Elétrica', 'Engenharia de produção'])

# Exibir seções restantes apenas quando um programa é selecionado
if capesselecionado != 'Escolha uma opção':
    st.title(f'CAPES - {capesselecionado}')
    if capesselecionado == 'Administração':
     subprocess.run(["streamlit","run", "c:/Users/thatt/Documents/Projeto_Streamlit/src/comparqualisAdm.py"])
    