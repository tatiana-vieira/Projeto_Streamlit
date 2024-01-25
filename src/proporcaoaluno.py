import matplotlib.pyplot as plt
import pandas as pd

# Seus dados
data = {
    'PPGs': ['Administração (MP)', 'Ciências e Engenharia de Materiais (M e D)', 'Ciência e Tecnologia da Computação (M)',
            'Desenvolvimento,Tecnologia e Sociedade (M)', 'Educação em Ciências (M)', 'Engenharia de Energia (M)',
            'Engenharia de Materiais (MP)', 'Engenharia Producação( M e D)', 'Engenharia de Produção (MP)',
            'Engenharia Elétrica (M e D)', 'Engenharia Hídrica (MP)', 'Engenharia Mecânica (M e D)', 'Física (M)',
            'Gestão e Regulação de Recursos Hídricos (MP)', 'Matemática (M)', 'Meio Ambiente e Recursos Hidricos (M)',
            'Multicêntrico em Química (M e D)', 'Proporção-aluno-funcionário'],
    '2018-2020': ['A', 'B', 'B', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'B', 'A', 'A', 'A', 'A', 'A', 'A', 'A'],
    '2019-2021': ['B', 'A', 'A', 'A', 'B', 'A', 'A', 'A', 'A', 'B', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A'],
    '2020-2022': ['B', 'A', 'A', 'A', 'C', 'A', 'A', 'A', 'A', 'B', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A']
}

# Criar um DataFrame a partir dos dados
df = pd.DataFrame(data)

# Mapear os conceitos para tamanhos de bolhas
size_map = {'A': 200, 'B': 100, 'C': 50}

# Configurar o gráfico de bolhas
fig, ax = plt.subplots(figsize=(10, 6))

for index, row in df.iterrows():
    for i, col in enumerate(['2018-2020', '2019-2021', '2020-2022']):
        concept = row[col]
        size = size_map.get(concept, 50)  # Use 50 como padrão para conceitos desconhecidos
        ax.scatter(index, i, color='green', s=size, label=concept if i == 0 else '')

# Adicionar rótulos e legendas
ax.set_xticks(range(len(df['PPGs'])))
ax.set_xticklabels(df['PPGs'], rotation=90, ha='right')
ax.set_yticks(range(3))
ax.set_yticklabels(['2018-2020', '2019-2021', '2020-2022'])
ax.set_ylabel('Ano')
ax.set_xlabel('PPGs')
ax.legend(title='Conceitos')

# Mostrar o gráfico
plt.show()





