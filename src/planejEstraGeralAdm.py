import streamlit as st

# Carregando a imagem
image = st.image('imagens\\adm.png', width=250)

# Define a cor do título
st.markdown(
    f'<style>h1 {{ color: #001F3F; }}</style>', 
    unsafe_allow_html=True
)

# Dicionário com objetivos, metas e indicadores
dados = {
    "Melhorar a qualidade do ensino": {
        "Metas": [
            "Aumentar a taxa de sucesso nos cursos",
            "Reduzir a taxa de evasão",
            "Aumentar a oferta dos cursos",
            "Aumentar percentual de docentes",
            "Aumentar a nota no PPG na CAPES"
        ],
        "Indicadores": {
            "Aumentar a taxa de sucesso nos cursos": "Taxa de sucesso nos cursos",
            "Reduzir a taxa de evasão": "Taxa de evasão",
            "Aumentar a oferta dos cursos": "Número de cursos",
            "Aumentar percentual de docentes": "Percentual de docentes com Pós-Doutorado",
            "Aumentar a nota no PPG na CAPES": "Nota no PPG na Avaliação Quadrienal da CAPES"
        }
    },
    "Promover a Modernização dos Cursos": {
        "Metas": [
            "Estruturação dos cursos"
        ],
        "Indicadores": {
            "Estruturação dos cursos": "Número de revisões nos PPCs dos cursos"
        }
    },
    "Promover a Internacionalização do ensino": {
        "Metas": [
            "Aumentar número discentes e docentes em atividade de internacionalização",
            "Aumentar número disciplinas ofertadas em língua estrangeira"
        ],
        "Indicadores": {
            "Aumentar número discentes e docentes em atividade de internacionalização": "Número envolvidos",
            "Aumentar número disciplinas ofertadas em língua estrangeira": "Número de disciplinas ofertadas"
        }
    }
}

# Página principal
#st.markdown("<h3 style='color: #001F3F;'>Planejamento Estratégico</h3>", unsafe_allow_html=True)
st.sidebar.header("Planejamento Estratégico")


# Escolha do Objetivo
st.sidebar.header("Objetivos:")
objetivo_escolhido = st.sidebar.selectbox("Escolha um objetivo:", list(dados.keys()))

# Exibindo Metas
st.sidebar.header("Metas:")
metas = dados[objetivo_escolhido]["Metas"]
meta_escolhida = st.sidebar.selectbox("Escolha uma meta:", metas)

# Exibindo Indicadores para a meta escolhida
st.sidebar.header("Indicadores:")
indicadores = dados[objetivo_escolhido]["Indicadores"][meta_escolhida]
st.sidebar.write(f"Indicador'{meta_escolhida}': {indicadores}")