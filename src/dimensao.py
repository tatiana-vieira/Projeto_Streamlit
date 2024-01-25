import streamlit as st

# Dicionário de dimensões, métricas e objetivos
dimensoes = {
    "Ensino e Aprendizagem": {
        "metricas": [
            "Proporção aluno-funcionário",
            "Graduação pontual(bacharelado)",
            "Graduação pontual(mestrado)",
            "Pessoal acadêmico com doutoramento",
            "Contato com ambiente de trabalho (bacharelado)",
            "Contato com ambiente de trabalho (mestrado)",
            "Equilíbrio de gênero"
        ],
        "objetivos": {
            "Proporção aluno-funcionário": ["Reduzir a proporção para melhorar o atendimento individual", "Manter uma proporção equilibrada"],
            "Graduação pontual(bacharelado)": ["Aumentar a taxa de graduação", "Melhorar a qualidade do ensino"],
            "Graduação pontual(mestrado)": ["Aumentar a taxa de graduação", "Fornecer suporte adicional aos estudantes"],
            "Pessoal acadêmico com doutoramento": ["Aumentar o número de professores com doutorado", "Garantir que 70% do pessoal tenha doutorado"],
            "Contato com ambiente de trabalho (bacharelado)": ["Aumentar o número de estudantes com experiência de trabalho", "Melhorar a qualidade das experiências"],
            "Contato com ambiente de trabalho (mestrado)": ["Aumentar o número de estudantes com experiência de trabalho", "Melhorar a qualidade das experiências"],
            "Equilíbrio de gênero": ["Alcançar equilíbrio de gênero de 50/50", "Promover a igualdade de gênero"]
        }
    },
    # Adicione mais dimensões, métricas e objetivos conforme necessário
     "Pesquisar": {
       "metricas": [
         "Receita pesquisa-externa",
         "Produtividade de doutorado",
         "Publicações pesquisa",
         "Taxa de citação",
         "Publicações mais citadas",
         "Publicações interdisciplinares",
         "Publicação de acesso aberto",
         "Orientação de pesquisa do ensino",
         "Autoras mulheres"  
        ],
        "objetivos": {
          "Receita pesquisa-externa": ["Aumentar a receita de pesquisa externa"],
          "Produtividade de doutorado": ["Aumentar a produtividade de doutorado", "Manter a produtividade de doutorado"],
          "Publicações pesquisa": ["Aumentar o número de publicações de pesquisa", "Manter o número de publicações de pesquisa"],
          "Taxa de citação": ["Aumentar a taxa de citação", "Manter a taxa de citação"],
          "Publicações mais citadas": ["Aumentar o número de publicações mais citadas", "Manter o número de publicações mais citadas"],
          "Publicações interdisciplinares": ["Aumentar o número de publicações interdisciplinares", "Manter o número de publicações interdisciplinares"],
          "Publicação de acesso aberto": ["Aumentar o número de publicações de acesso aberto", "Manter o número de publicações de acesso aberto"],
          "Orientação de pesquisa do ensino": ["Aumentar a orientação de pesquisa do ensino", "Manter a orientação de pesquisa do ensino"],
          "Autoras mulheres": ["Aumentar a presença de autoras mulheres", "Manter a presença de autoras mulheres"]
        }
    },
    # Adicione mais dimensões, métricas e objetivos conforme necessário
     "Transferência de Conhecimento":{
       "metricas": [
         "Renda de fontes privadas",
         "Co-publicações com parceiros industriais",
         "Publicações citadas em patentes"
       ],
       "objetivos": {
        "Renda de fontes privadas": ["Aumentar a renda de fontes privadas", "Manter a renda de fontes privadas"],
        "Co-publicações com parceiros industriais": ["Aumentar o número de co-publicações com parceiros industriais", "Manter o número de co-publicações"],
        "Publicações citadas em patentes": ["Aumentar o número de publicações citadas em patentes", "Manter o número de publicações citadas em patentes"]
       }
    },
    # Adicione mais dimensões, métricas e objetivos conforme necessário
      "Orientação Internacional": {
       "metricas": [
         "Orientação Internacional de programa (bacharelado)",
         "Orientação Internacional de programa (mestrado)",
         "Oportunidades de estudar no exterior",
         "Doutorado internacional",
         "Publicação conjuntas internacionais",
         "Bolsas de pesquisas internacionais"
       ],
       "objetivos": {
         "Orientação Internacional de programa (bacharelado)":["Aumentar a orientação internacional para programas de bacharelado", "Manter a qualidade da orientação internacional em programas de bacharelado"],
         "Orientação Internacional de programa (mestrado)":["Melhorar a orientação internacional para programas de mestrado","Garantir que programas de mestrado tenham orientação internacional de alta qualidade"],
         "Oportunidades de estudar no exterior":["Aumentar as oportunidades para estudantes estudarem no exterior","Garantir que os estudantes tenham acesso a oportunidades de estudo no exterior"],
         "Doutorado internacional":["Aumentar a internacionalização dos programas de doutorado","Promover programas de doutorado internacional de alta qualidade"],
         "Publicação conjuntas internacionais":["Aumentar a colaboração em publicações internacionais","Manter a qualidade das publicações conjuntas internacionais"],
         "Bolsas de pesquisas internacionais":["Aumentar o acesso a bolsas de pesquisas internacionais","Garantir que os pesquisadores tenham acesso a oportunidades de pesquisa internacional"]
        }
    },
    "Engajamento Regional": {
     "metricas": [ 
        "Estágios estudantis na região",
        "Publicações conjuntas regionais",
        "Rendas de fontes regionais"
      ],
     "objetivos": {
       "Estágios estudantis na região": ["Aumentar o número de estágios estudantis na região","Fomentar oportunidades de estágio para estudantes na região" ],
       "Publicações conjuntas regionais": ["Promover a colaboração regional em publicações","Aumentar a qualidade das publicações conjuntas regionais"],
       "Rendas de fontes regionais": ["Aumentar as fontes de receita regionais","Garantir sustentabilidade financeira por meio de fontes regionais" ]
         
      }
    }
}
   
# Título da página
st.title("Coordenação de Programas")

# Seleção da dimensão
dimensao_selecionada = st.selectbox("Selecione a Dimensão", list(dimensoes.keys()))

# Seleção da métrica
metrica_selecionada = st.selectbox("Selecione a Métrica", dimensoes[dimensao_selecionada]["metricas"])

# Seleção do objetivo
objetivo_selecionado = st.selectbox("Selecione o Objetivo", dimensoes[dimensao_selecionada]["objetivos"][metrica_selecionada])

# Caixa de texto para medidas (se necessário)
if "medida" in metrica_selecionada.lower():
    medida = st.number_input("Medida (porcentagem)", min_value=0, max_value=100, step=1)

# Botão para gerar resultados
if st.button("Gerar Resultados"):
    st.write("Dimensão selecionada:", dimensao_selecionada)
    st.write("Métrica selecionada:", metrica_selecionada)
    st.write("Objetivo selecionado:", objetivo_selecionado)
    if "medida" in metrica_selecionada.lower():
        st.write("Medida selecionada:", medida)
