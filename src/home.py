from PIL import Image
import streamlit as st
import numpy as np
import os

# Carregando a imagem
image = Image.open('imagens\\PPG.png')

# Definindo o layout em duas colunas
col1, col2,col3,col4,col5 = st.columns([1,1,1,3,1])  # A primeira coluna ocupa 1 unidade, a segunda 3 unidades

# Primeira coluna: imagem centralizada
#col4.image(image,width=100)
col4.image(image,use_column_width=50)
#Definindo o estilo CSS para o título
titulo_style = """
<style>
  h1{
   text-align:center;
   color:#00498b; #cor azul escuro
  }
"""
st.markdown(titulo_style,unsafe_allow_html=True)

col1,col2,col3 = st.columns (3)

programaselecionado = st.sidebar.selectbox('Selecione um programa de pós : ',['Administração','Ciência e Engenharia de Materiais','Ciência e Tecnologia da Informação','Engenharia Elétrica', 'Engenharia de produção'])
#Criar programas no selecbox
if programaselecionado == 'Administração':
     st.title ('Mestrado Profissional em Administração')
elif programaselecionado == 'Ciência e Engenharia de Materiais':
     st.title ('Mestrado Profissional em Materiais para Engenharia')

####################################################################################################
dimensãoselecionado = st.sidebar.selectbox('Selecione uma dimensão: ',['Ensino e Aprendizagem','Pesquisar','Engajamento Regional','Orientação Internaciona', 'Geral'])

#Criar Dimensão no selecbox
if dimensãoselecionado == 'Ensino e Aprendizagem':
     st.title ('Ensino e Aprendizagem')
elif dimensãoselecionado == 'Pesquisar':
     st.title ('Pesquisar')
elif dimensãoselecionado == 'Engajamento Regional':
     st.title ('Engajamento Regional')
elif dimensãoselecionado == 'Orientação Internacional':
     st.title ('Orientação Internacional')   
elif dimensãoselecionado == 'Geral':
     st.title ('Geral') 
#######################################################################################################
Coordenadorselecionado = st.sidebar.selectbox('Selecione uma Opção para Coordenador: ',['Escolha uma opção','Cadastrar Objetivo','Criar Metas','Gerenciar Metas','Medir Ações'])

#Criar Coordenador no selecbox
if Coordenadorselecionado == 'Cadastrar Objetivo':
     st.title ('Cadastrar Objetivo')
elif Coordenadorselecionado == 'Criar Metas':
     st.title ('Criar Metas')
elif Coordenadorselecionado == 'Gerenciar Metas':
     st.title ('Gerenciar Metas')
elif Coordenadorselecionado == 'Medir Ações':
     st.title ('Medir Ações')   
#######################################################################################################

# Carregando a imagem docente
image_docente = Image.open('imagens\\professor.png')
# Carregando a imagem producao Relevante
image_producaorelevante = Image.open('imagens\\ideia.png')
# Carregando a imagem producao Relevante
#image_multirank = Image.open('imagens\transferir.png')
image_multirank_path = os.path.join('imagens', 'transferir.png')
image_multirank = Image.open(image_multirank_path)

# Definindo o layout em duas colunas
col1, col2,col3= st.columns([1,1,1])

with col1:
 if st.button('Docentes',key='botao1', help='Docente'):
    st.markdown("[Clique aqui para acessar a página de Docentes]")
      
 st.image(image_docente,width=70)
 st.markdown("&nbsp;", unsafe_allow_html=True)  # Adicionando espaço vertical

 
with col2:
  if st.button('Producões Relevantes',key='botao2'):
      pass
  st.image(image_producaorelevante,width=70)
  st.markdown("&nbsp;", unsafe_allow_html=True)  # Adicionando espaço vertical


with col3:
  if st.button('Simulações U-Multirank', key='botao3'):
      pass
  st.image(image_multirank,width=70)
  st.markdown("&nbsp;", unsafe_allow_html=True)  # Adicionando espaço vertical

#Carregando as imagens de baixo
image_discente = Image.open('imagens\\aluno.png')
# Carregando a imagem producao Relevante
image_engajamento = Image.open('imagens\\mundo.png')
# Carregando a imagem producao Relevante
image_comparar = Image.open('imagens\\comparar.png')


 #Adicionar mais três imagens abaixo das anteriores
col4, col5, col6 = st.columns([1, 1, 1])

with col4:
 if st.button('Discentes',key='botao4', help='Discentes'):
      #Ação ao clicar no botão
      pass
 st.image(image_discente,width=70)
 st.markdown("&nbsp;", unsafe_allow_html=True)  # Adicionando espaço vertical


with col5:
 if st.button('Engajamento Regional',key='botao5', help='Engajamento Regional'):
      #Ação ao clicar no botão
      pass
 st.image(image_engajamento,width=70)
 st.markdown("&nbsp;", unsafe_allow_html=True)  # Adicionando espaço vertical

with col6:
 if st.button('Engajamento Regional',key='botao6', help='Comparação'):
      #Ação ao clicar no botão
      pass
 st.image(image_comparar,width=70)
 st.markdown("&nbsp;", unsafe_allow_html=True)  # Adicionando espaço vertical
