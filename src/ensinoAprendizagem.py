import streamlit as st
import pandas as pd


from utils.conect import conectar,fechar_conexao

#Inicialize as variáveis
contg = 0
contm = 0
count = 0
countt = 0


# Exemplo de uso
conn = conectar()

if conn:
    try:
        cursor = conn.cursor()

        # Executar a primeira consulta
        cursor.execute("SELECT * FROM discente;")
        discente = cursor.fetchall()

        # Executar a segunda consulta
        cursor.execute("SELECT * FROM docente;")
        docente = cursor.fetchall()

    finally:
        # Certifique-se de fechar a conexão e o cursor quando terminar
        fechar_conexao(conn)



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
ano_selecionado = st.sidebar.selectbox("Selecione o Ano", [2020, 2021, 2022, 2023, 2024])

# Seleção da Dimensão
dimensao_selecionada = st.sidebar.selectbox("Selecione a Dimensão", list(dimensoes.keys()))

# Seleção da Métrica
metrica_selecionada = st.sidebar.selectbox("Selecione a Métrica", dimensoes[dimensao_selecionada]["metricas"])

# Botão para gerar resultados
if st.sidebar.button("Gerar Resultados"):
   st.write("Ano selecionado:", ano_selecionado)
   st.write("Dimensão selecionada:", dimensao_selecionada)
   st.write("Métrica selecionada:", metrica_selecionada)

    # Verifique se a métrica selecionada possui objetivos
   if metrica_selecionada == "Proporção aluno-funcionário":
     #realiza cálculo 
      if ano_selecionado == 2020:
         for index, row in discente.iterrows():
          if (row["anosituacao"] == 2016) or (row["anosituacao"] == 2017) or (row["anosituacao"] == 2018) and (row["situacao"] != "DESLIGADO"):
             contg +=1
          elif (row["Nivel"] == "mestrado") or (row["Nivel"] == "mestrado profissional") :
             contm +=1
         for index, row in docente.iterrows():
          if (row["anocoleta"]==2016) or (row["anocoleta"]==2017)or (row["anocoleta"]==2018):
            count = count+1

         resultado = contm + (contg * 0.5) / count
     
      elif ano_selecionado == 2021:
        
        for index, row in discente.iterrows():
         if (row["anosituacao"] == 2017) or (row["anosituacao"] == 2018) or (row["anosituacao"] == 2019) and (row["situacao"] != "DESLIGADO"):
            if row["nivel"] == "graduação" :
               contg = contg +1
            elif row["nivel"] == "mestrado" :
               contm = contm +1
        for index, row in docente.iterrows():
          if (row["anocoleta"]==2017) or (row["anocoleta"]==2018)or (row["anocoleta"]==2019):
            count = count+1

        resultado = contm + (contg * 0.5) / count
       
        
      elif ano_selecionado == 2022:
        for index, row in discente.iterrows():
          if (row["anocoleta"] == 2018) or (row["anocoleta"] == 2019) or (row["anocoleta"] == 2020) and (row["Situacao"] != "DESLIGADO"):
             if row["Nivel"] == "Graduação" :
                contg = contg +1
             elif row["Nivel"] == "Mestrado" :
                contm = contm +1
        for index, row in docente.iterrows():
          if (row["anobase"]==2018) or (row["anobase"]==2019)or (row["anobase"]==2020):
            count = count+1

        resultado = contm + (contg * 0.5) / count
         
      elif ano_selecionado == 2023:
         for index, row in discente.iterrows():
           if (row["anocoleta"] == 2019) or (row["anocoleta"] == 2020) or (row["anocoleta"] == 2021) and (row["Situacao"] != "DESLIGADO"):
            if row["Nivel"] == "Graduação" :
               contg = contg +1
            elif row["Nivel"] == "Mestrado" :
               contm = contm +1
         for index, row in docente.iterrows():         
           if (row["anocoleta"]==2019) or (row["anocoleta"]==2020)or (row["anocoleta"]==2021):
             count = count+1

         resultado = contm + (contg * 0.5) / count
      
      elif ano_selecionado == 2024:
         for index, row in discente.iterrows():
           if (row["anosituacao"] == 2020) or (row["anocoleta"] == 2021) or (row["anocoleta"] == 2022) and (row["Situacao"] != "DESLIGADO"):
            if row["nivel"] == "Graduação" :
               contg = contg +1
            elif row["nivel"] == "Mestrado" :
               contm = contm +1
         for index, row in docente.iterrows():         
           if (row["anocoleta"]==2019) or (row["anocoleta"]==2020)or (row["anocoleta"]==2021):
             count = count+1

         resultado = contm + (contg * 0.5) / count
     
      st.write(f"Resultado da métrica: '{metrica_selecionada}'para o ano {ano_selecionado}: {resultado}")
   ## Verifique se a métrica selecionada possui objetivos
    # Verifique se a métrica selecionada possui objetivos
   if metrica_selecionada == "Mestrado Pontual":
      contTC=0
      contMA=0
      #realiza cálculo 
      if ano_selecionado == 2020:
       ano_inicial =2018
       anofinal =2020
       for index, row in discente.iterrows():
           if (row["anosituacao"] == 2020) and (row["Situacao"] == "TITULADO"):
             
             if ((row["anomatricula"]) >= ano_inicial ):
                contTC +=1
                
             elif ((row["anomatricula"]) < ano_inicial):
                contMA += 1
                
            
           if  (contTC != 0) and (contMA!= 0):  # Verifica se contMA não é zero para evitar divisão por zero
                  resultado = ((contTC) / contMA) * 100
           elif (contMA == 0) or (contTC == 0):
                  resultado = "Divisão por zero não é permitida."
           elif (contTC != 0) and (contMA == 0) :
                  resultado = "Formandos no tempo certo 100%: ",contTC
           elif (contTC == 0) and (contMA != 0):
                  resultado = "Formandos além do tempo : ", contMA
      
       st.write(f"Resultado da métrica: '{metrica_selecionada}'para o ano {ano_selecionado}: {resultado}")
      elif ano_selecionado == 2021:
       ano_inicial =2019
       anofinal =2021
       for index, row in discente.iterrows():
            if (row["anosituacao"] == 2021) and (row["Situacao"] == "TITULADO"):
             
              if ((row["anomatricula"]) >= ano_inicial ):
                contTC +=1
                
              elif ((row["anomatricula"]) < ano_inicial):
                contMA += 1
                
               
              if  (contTC != 0) and (contMA!= 0):  # Verifica se contMA não é zero para evitar divisão por zero
                  resultado = (contTC / contMA) * 100
              elif (contMA == 0) or (contTC == 0):
                  resultado = "Divisão por zero não é permitida."
              elif (contTC != 0) and (contMA == 0) :
                  resultado = "Formandos no tempo certo 100%: ",contTC
              elif (contTC == 0) and (contMA != 0):
                   resultado = "Formandos além do tempo : ", contMA
         
       st.write(f"Resultado da métrica: '{metrica_selecionada}'para o ano {ano_selecionado}: {resultado}")
      elif ano_selecionado == 2022:
       ano_inicial =2020
       anofinal =2022
       for index, row in discente.iterrows():
           if (row["anosituacao"] == 2022) and (row["Situacao"] == "TITULADO"):
             
             if ((row["anomatricula"]) >= ano_inicial ):
                contTC +=1
                
             elif ((row["anomatricula"]) < ano_inicial):
                contMA += 1
                
               
             if  (contTC != 0) and (contMA!= 0):  # Verifica se contMA não é zero para evitar divisão por zero
                  resultado = (contTC / contMA) * 100
             elif (contMA == 0) or (contTC == 0):
                  resultado = "Divisão por zero não é permitida."
             elif (contTC != 0) and (contMA == 0) :
                  resultado = "Formandos no tempo certo 100%: ",contTC
             elif (contTC == 0) and (contMA != 0):
                   resultado = "Formandos além do tempo : ", contMA
         
       st.write(f"Resultado da métrica: '{metrica_selecionada}'para o ano {ano_selecionado}: {resultado}")
    # Verifique se a métrica selecionada possui objetivos
   if metrica_selecionada == "Pessoal acadêmico com doutoramento":
     #realiza cálculo 
      if ano_selecionado == 2020:
         for index, row in discente.iterrows():
          if (row["anosituacao"] == 2016) or (row["anosituacao"] == 2017) or (row["anosituacao"] == 2018) and (row["situacao"] != "DESLIGADO"):
             contg +=1
          elif row["nivel"] == "Mestrado" :
             contm +=1
         for index, row in docente.iterrows():
          if (row["anobase"]==2016) or (row["anobase"]==2017)or (row["anobase"]==2018):
            count = count+1

         resultado = contm + (contg * 0.5) / count
     
      elif ano_selecionado == 2021:
        
        for index, row in discente.iterrows():
         if (row["anocoleta"] == 2017) or (row["anocoleta"] == 2018) or (row["anocoleta"] == 2019) and (row["Situacao"] != "DESLIGADO"):
            if row["nivel"] == "Graduação" :
               contg = contg +1
            elif row["nivel"] == "Mestrado" :
               contm = contm +1
        for index, row in docente.iterrows():
          if (row["anobase"]==2017) or (row["anobase"]==2018)or (row["anobase"]==2019):
            count = count+1

        resultado = contm + (contg * 0.5) / count
       
        
      elif ano_selecionado == 2022:
        for index, row in discente.iterrows():
          if (row["anocoleta"] == 2018) or (row["anocoleta"] == 2019) or (row["anocoleta"] == 2020) and (row["situacao"] != "DESLIGADO"):
             if row["nivel"] == "Graduação" :
                contg = contg +1
             elif row["nivel"] == "Mestrado" :
                contm = contm +1
        for index, row in docente.iterrows():
          if (row["anobase"]==2018) or (row["anobase"]==2019)or (row["anobase"]==2020):
            count = count+1

        resultado = contm + (contg * 0.5) / count
         
      elif ano_selecionado == 2023:
         for index, row in discente.iterrows():
           if (row["anocoleta"] == 2019) or (row["anocoleta"] == 2020) or (row["anocoleta"] == 2021) and (row["situacao"] != "DESLIGADO"):
            if row["nivel"] == "Graduação" :
               contg = contg +1
            elif row["nivel"] == "Mestrado" :
               contm = contm +1
         for index, row in docente.iterrows():         
           if (row["anobase"]==2019) or (row["anobase"]==2020)or (row["anobase"]==2021):
             count = count+1

         resultado = contm + (contg * 0.5) / count
      
      elif ano_selecionado == 2024:
         for index, row in discente.iterrows():
           if (row["anosituacao"] == 2020) or (row["anocoleta"] == 2021) or (row["anocoleta"] == 2022) and (row["situacao"] != "DESLIGADO"):
            if row["nivel"] == "Graduação" :
               contg = contg +1
            elif row["nivel"] == "Mestrado" :
               contm = contm +1
         for index, row in docente.iterrows():         
           if (row["anobase"]==2019) or (row["anobase"]==2020)or (row["anobase"]==2021):
             count = count+1

         resultado = contm + (contg * 0.5) / count
     
      st.write(f"Resultado da métrica: '{metrica_selecionada}'para o ano {ano_selecionado}: {resultado}")
   if metrica_selecionada == "Contato com ambiente de trabalho (mestrado)":
     #realiza cálculo 
      if ano_selecionado == 2020:
         for index, row in discente.iterrows():
          if (row["anosituacao"] == 2016) or (row["anosituacao"] == 2017) or (row["anosituacao"] == 2018) and (row["situacao"] != "DESLIGADO"):
             contg +=1
          elif row["nivel"] == "Mestrado" :
             contm +=1
         for index, row in docente.iterrows():
          if (row["anobase"]==2016) or (row["anobase"]==2017)or (row["anobase"]==2018):
            count = count+1

         resultado = contm + (contg * 0.5) / count
     
      elif ano_selecionado == 2021:
        
        for index, row in discente.iterrows():
         if (row["anocoleta"] == 2017) or (row["anocoleta"] == 2018) or (row["anocoleta"] == 2019) and (row["situacao"] != "DESLIGADO"):
            if row["nivel"] == "Graduação" :
               contg = contg +1
            elif row["nivel"] == "Mestrado" :
               contm = contm +1
        for index, row in docente.iterrows():
          if (row["anobase"]==2017) or (row["anobase"]==2018)or (row["anobase"]==2019):
            count = count+1

        resultado = contm + (contg * 0.5) / count
       
        
      elif ano_selecionado == 2022:
        for index, row in discente.iterrows():
          if (row["anocoleta"] == 2018) or (row["anocoleta"] == 2019) or (row["anocoleta"] == 2020) and (row["situacao"] != "DESLIGADO"):
             if row["nivel"] == "Graduação" :
                contg = contg +1
             elif row["nivel"] == "Mestrado" :
                contm = contm +1
        for index, row in docente.iterrows():
          if (row["anobase"]==2018) or (row["anobase"]==2019)or (row["anobase"]==2020):
            count = count+1

        resultado = contm + (contg * 0.5) / count
         
      elif ano_selecionado == 2023:
         for index, row in discente.iterrows():
           if (row["anocoleta"] == 2019) or (row["anocoleta"] == 2020) or (row["anocoleta"] == 2021) and (row["situacao"] != "DESLIGADO"):
            if row["nivel"] == "Graduação" :
               contg = contg +1
            elif row["nivel"] == "Mestrado" :
               contm = contm +1
         for index, row in docente.iterrows():         
           if (row["anobase"]==2019) or (row["anobase"]==2020)or (row["anobase"]==2021):
             count = count+1

         resultado = contm + (contg * 0.5) / count
      
      elif ano_selecionado == 2024:
         for index, row in discente.iterrows():
           if (row["anosituacao"] == 2020) or (row["anocoleta"] == 2021) or (row["anocoleta"] == 2022) and (row["situacao"] != "DESLIGADO"):
            if row["nivel"] == "Graduação" :
               contg = contg +1
            elif row["nivel"] == "Mestrado" :
               contm = contm +1
         for index, row in docente.iterrows():         
           if (row["anobase"]==2019) or (row["anobase"]==2020)or (row["anobase"]==2021):
             count = count+1

         resultado = contm + (contg * 0.5) / count
     
      st.write(f"Resultado da métrica: '{metrica_selecionada}'para o ano {ano_selecionado}: {resultado}")
      
   if metrica_selecionada == "Equilíbrio de gênero":
      alunoMasc =0
      alunoFem=0
      TMasc=0
      TFem=0
      TaxaFem = 0
      TaxaMasc = 0
     #realiza cálculo 
      if ano_selecionado == 2020:
         for index, row in discente.iterrows():
          if (row["anosituacao"] == 2016) or (row["anosituacao"] == 2017) or (row["anosituacao"] == 2018) and (row["situacao"] != "DESLIGADO"):
             if (row["situacao"] == "MATRICULADO"): 
                if (row["sexo"] == "Masculino"):
                     alunoMasc = alunoMasc +1
                elif (row["Sexo"] == "Feminino"):
                     alunoFem = alunoFem  +1
             elif (row["Situacao"] == "TITULADO"): 
                if (row["sexo"] == "Masculino"):
                     TMasc = alunoMasc +1
                elif (row["sexo"] == "Feminino"):
                     TFem = alunoFem  +1
      elif ano_selecionado == 2021:
         for index, row in discente.iterrows():
          if (row["anosituacao"] == 2017) or (row["anosituacao"] == 2018) or (row["anosituacao"] == 2019) and (row["situacao"] != "DESLIGADO"):
             if (row["situacao"] == "MATRICULADO"): 
                if (row["sexo"] == "Masculino"):
                     alunoMasc = alunoMasc +1
                elif (row["sexo"] == "Feminino"):
                     alunoFem = alunoFem  +1
             elif (row["situacao"] == "TITULADO"): 
                if (row["sexo"] == "Masculino"):
                     TMasc = alunoMasc +1
                elif (row["sexo"] == "Feminino"):
                     TFem = alunoFem  +1
      elif ano_selecionado == 2022:
         for index, row in discente.iterrows():
          if (row["anosituacao"] == 2018) or (row["anosituacao"] == 2019) or (row["anosituacao"] == 2020) and (row["situacao"] != "DESLIGADO"):
             if (row["situacao"] == "MATRICULADO"): 
                if (row["sexo"] == "Masculino"):
                     alunoMasc = alunoMasc + 1
                elif (row["sexo"] == "Feminino"):
                     alunoFem = alunoFem  + 1
             elif (row["Situacao"] == "TITULADO"): 
                if (row["sexo"] == "Masculino"):
                     TMasc = alunoMasc + 1
                elif (row["sexo"] == "Feminino"):
                     TFem = alunoFem  + 1
      elif ano_selecionado == 2023:
         for index, row in discente.iterrows():
          if (row["anosituacao"] == 2019) or (row["anosituacao"] == 2020) or (row["anosituacao"] == 2021) and (row["situacao"] != "DESLIGADO"):
             if (row["Situacao"] == "MATRICULADO"): 
                if (row["sexo"] == "Masculino"):
                     alunoMasc = alunoMasc + 1
                elif (row["Sexo"] == "Feminino"):
                     alunoFem = alunoFem  + 1
             elif (row["situacao"] == "TITULADO"): 
                if (row["sexo"] == "Masculino"):
                     TMasc = alunoMasc + 1
                elif (row["sexo"] == "Feminino"):
                     TFem = alunoFem + 1
      elif ano_selecionado == 2024:
         for index, row in discente.iterrows():
          if (row["anosituacao"] == 2020) or (row["anosituacao"] == 2021) or (row["anosituacao"] == 2022) and (row["situacao"] != "DESLIGADO"):
             if (row["situacao"] == "MATRICULADO"): 
                if (row["sexo"] == "Masculino"):
                     alunoMasc = alunoMasc + 1
                elif (row["sexo"] == "Feminino"):
                     alunoFem = alunoFem  + 1
             elif (row["situacao"] == "TITULADO"): 
                if (row["sexo"] == "Masculino"):
                     TMasc = alunoMasc + 1
                elif (row["sexo"] == "Feminino"):
                     TFem = alunoFem + 1

      TaxaFem = TFem / alunoFem
      TaxaMasc = TMasc / alunoMasc
      Resultado = TaxaFem / TaxaMasc
      st.write(f"Resultado do Equilíbrio de Gênero:  '{Resultado}' para o ano {ano_selecionado}")


  



