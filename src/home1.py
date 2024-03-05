from PIL import Image
import streamlit as st
import os
import subprocess

# Set a fixed width for buttons
button_width = 150

# Set a fixed size for images
image_width = 100

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

# Criar programas no selecbox
if programaselecionado == 'Administração':
    st.title('Mestrado Profissional em Administração')
elif programaselecionado == 'Ciência e Engenharia de Materiais':
    st.title('Mestrado Profissional em Materiais para Engenharia')

####################################################################################################
dimensãoselecionado = st.sidebar.selectbox('Selecione uma dimensão do U-Multirank: ',
                                          ['Escolha uma opção','Ensino e Aprendizagem', 'Pesquisar', 'Engajamento Regional', 'Orientação Internacional', 'Geral'])

# Criar Dimensão no selecbox
if dimensãoselecionado == 'Ensino e Aprendizagem':
    st.title('Ensino e Aprendizagem')
elif dimensãoselecionado == 'Pesquisar':
    st.title('Pesquisar')
elif dimensãoselecionado == 'Engajamento Regional':
    st.title('Engajamento Regional')
elif dimensãoselecionado == 'Orientação Internacional':
    st.title('Orientação Internacional')
elif dimensãoselecionado == 'Geral':
    st.title('Geral')
##################################################################################################################
capesselecionado = st.sidebar.selectbox('Selecione um programa da CAPES: ',
                                          ['Escolha uma opção','Administração', 'Ciência e Engenharia de Materiais', 'Ciência e Tecnologia da Informação', 'Engenharia Elétrica', 'Engenharia de produção'])

######################################################################################################

# Carregando a imagem docente
image_docente = Image.open('imagens\\professor.png')
# Carregando a imagem producao Relevante
image_producaorelevante = Image.open('imagens\\ideia.png')
# Carregando a imagem producao Relevante
image_pdi = Image.open('imagens\\pdi1.png')
# image_multirank_path = os.path.join('imagens', 'transferir.png')
image_multirank_path = os.path.join('imagens', 'multi.png')
image_multirank = Image.open(image_multirank_path)

# Definindo o layout em duas colunas
col1, col2, col3, col4 = st.columns([1, 1, 1, 1])

with col1:
    if st.button('Professor'):
        st.markdown(
            f'<button style="width: {button_width}px">Docentes</button>',
            unsafe_allow_html=True
        )
        if programaselecionado == 'Administração':
            subprocess.run(["streamlit", "run", "c:/Users/thatt/Documents/Projeto_Streamlit/src/docente_adm.py"])
        elif programaselecionado == 'Ciência e Engenharia de Materiais':
            st.write('Conteúdo específico para Produções Relevantes em Ciência e Engenharia de Materiais')
        # Add conditions for other programs as needed
    st.image(image_docente, width=image_width)
    st.markdown("&nbsp;", unsafe_allow_html=True)

with col2:
    if st.button('Produção Relevante'):
        st.markdown(
            f'<button style="width: {button_width}px">Produções Relevantes</button>',
            unsafe_allow_html=True
        )
        # Conteúdo específico para 'Produções Relevantes' no programa selecionado
        if programaselecionado == 'Administração':
            subprocess.run(["streamlit", "run", "c:/Users/thatt/Documents/Projeto_Streamlit/src/Prodrelevanteadm.py"])
        elif programaselecionado == 'Ciência e Engenharia de Materiais':
            st.write('Conteúdo específico para Produções Relevantes em Ciência e Engenharia de Materiais')
        # Adicione condições para outros programas conforme necessário

    st.image(image_producaorelevante, width=image_width)
    st.markdown("&nbsp;", unsafe_allow_html=True)  # Adicionando espaço vertical

with col3:
    if st.button('PDI'):
        st.markdown(
            f'<button style="width: {button_width}px">PDI</button>',
            unsafe_allow_html=True
        )
        if programaselecionado == 'Administração':
            subprocess.run(["streamlit","run", "c:/Users/thatt/Documents/Projeto_Streamlit/src/SimUmAdm.py"])
        elif programaselecionado == 'Ciência e Engenharia de Materiais':
            st.write('Conteúdo específico para Simulações U-Multirank em Ciência e Engenharia de Materiais')
        # Adicione condições para outros programas conforme necessário

    st.image(image_pdi, width=image_width)
    st.markdown("&nbsp;", unsafe_allow_html=True)  # Adicionando espaço vertical

with col4:
    if st.button('Avaliação Multidimensional'):
        st.markdown(
            f'<button style="width: {button_width}px">Avaliação Multidimensional</button>',
            unsafe_allow_html=True
        )
        if programaselecionado == 'Administração':
            subprocess.run(["streamlit","run", "c:/Users/thatt/Documents/Projeto_Streamlit/src/SimUmAdm.py"])
        elif programaselecionado == 'Ciência e Engenharia de Materiais':
            st.write('Conteúdo específico para Simulações U-Multirank em Ciência e Engenharia de Materiais')
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
            f'<button style="width: {button_width}px">Discentes</button>',
            unsafe_allow_html=True
        )
        # Conteúdo específico para 'Discentes' no programa selecionado
        if programaselecionado == 'Administração':
            subprocess.run(["streamlit","run", "c:/Users/thatt/Documents/Projeto_Streamlit/src/discente_adm.py"])
        elif programaselecionado == 'Ciência e Engenharia de Materiais':
            st.write('Conteúdo específico para Discentes em Ciência')
    st.image(image_discente, width=70)
    st.markdown("&nbsp;", unsafe_allow_html=True)  # Adicionando espaço vertical

with col6:
    if st.button('Engajamento Regional'):
        st.markdown(
            f'<button style="width: {button_width}px">Engajamento Regional</button>',
            unsafe_allow_html=True
        )
        if programaselecionado == 'Administração':
            st.write('Conteúdo específico para Discentes em Administração')
        elif programaselecionado == 'Ciência e Engenharia de Materiais':
            st.write('Conteúdo específico para Discentes em Ciência')
    st.image(image_engajamento, width=70)
    st.markdown("&nbsp;", unsafe_allow_html=True)  # Adicionando espaço vertical

with col7:
    if st.button('Comparação'):
        st.markdown(
            f'<button style="width: {button_width}px">Comparação</button>',
            unsafe_allow_html=True
        )
        if programaselecionado == 'Administração':
            st.write('Conteúdo específico para Discentes em Administração')
        elif programaselecionado == 'Ciência e Engenharia de Materiais':
            st.write('Conteúdo específico para Discentes em Ciência')
    st.image(image_comparar, width=70)
    st.markdown("&nbsp;", unsafe_allow_html=True)  # Adicionando espaço vertical

with col8:
    if st.button('Planejamento'):
        st.markdown(
            f'<button style="width: {button_width}px">Planejamento Estratégico</button>',
            unsafe_allow_html=True
        )
        if programaselecionado == 'Administração':
            st.write('Conteúdo específico para Discentes em Administração')
        elif programaselecionado == 'Ciência e Engenharia de Materiais':
            st.write('Conteúdo específico para Discentes em Ciência')
    st.image(image_planejamento, width=image_width)
    st.markdown("&nbsp;", unsafe_allow_html=True)  # Adicionando espaço vertical