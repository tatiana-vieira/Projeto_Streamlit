import matplotlib.pyplot as plt
import pandas as pd

# Seus dados
data = {
    'PPGs': ['Administração (MP)', 'Ciências e Engenharia de Materiais (M e D)', 'Ciência e Tecnologia da Computação (M)',
            'Desenvolvimento,Tecnologia e Sociedade (M)', 'Educação em Ciências (M)', 'Engenharia de Energia (M)',
            'Engenharia de Materiais (MP)', 'Engenharia Producação( M e D)', 'Engenharia de Produção (MP)',
            'Engenharia Elétrica (M e D)', 'Engenharia Hídrica (MP)', 'Engenharia Mecânica (M e D)', 'Física (M)',
            'Gestão e Regulação de Recursos Hídricos (MP)', 'Matemática (M)', 'Meio Ambiente e Recursos Hidricos (M)',
            'Multicêntrico em Química (M e D)'],
    'Mestrado Pontual': ['B', 'B', 'C', 'C', 'A', 'B', 'C', 'B', 'B', 'B', 'C', 'B', 'B', 'B', 'A', 'B', 'B'],
    '2018-2020': ['B', 'B', 'B', 'B', 'A', 'C', 'C', 'A', 'B', 'B', 'C', 'B', 'B', 'B', 'A', 'B', 'B'],
    '2019-2021': ['B', 'B', 'B', 'B', 'A', 'C', 'C', 'B', 'B', 'B', 'C', 'B', 'B', 'B', 'A', 'B', 'B'],
    '2020-2022': ['B', 'B', 'B', 'B', 'D', 'E', 'A', 'B', 'C', 'B', 'C', 'C', 'B', 'B', 'B', 'A', 'B']
}

# Criar um DataFrame a partir dos dados
df = pd.DataFrame(data)

# Mapear os conceitos para tamanhos de bolhas
size_map = {'A': 200, 'B': 100, 'C': 50, 'D': 30, 'E': 20}

# Mapear as letras para cores
color_map = {'A': 'green', 'B': 'orange', 'C': 'red', 'D': 'blue', 'E': 'purple'}

# Configurar o gráfico de bolhas
fig, ax = plt.subplots(figsize=(10, 6))
legend_shown = set()  # Conjunto para rastrear quais conceitos já foram adicionados à legenda

for index, row in df.iterrows():
    for i, col in enumerate(['2018-2020', '2019-2021', '2020-2022']):
        concept = row[col]
        size = size_map.get(concept, 30)  # Use 30 como padrão para conceitos desconhecidos
        if concept not in legend_shown:
            ax.scatter([], [], color=color_map[concept], s=size, label=concept)
            legend_shown.add(concept)
        ax.scatter(index, i, color=color_map[concept], s=size)

# Adicionar rótulos e legendas
ax.set_xticks(range(len(df['PPGs'])))
ax.set_xticklabels(df['PPGs'], rotation=90, ha='right')
ax.set_yticks(range(3))
ax.set_yticklabels(['2018-2020', '2019-2021', '2020-2022'])
ax.set_ylabel('Ano')
ax.set_xlabel('PPGs')

# Mover a legenda para a parte superior do gráfico
ax.legend(title='Conceitos', bbox_to_anchor=(1.05, 1), loc='upper left')

# Ajustar o layout para evitar corte
plt.tight_layout()

# Mostrar o gráfico
plt.show()





