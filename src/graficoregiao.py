import geopandas as gpd
import matplotlib.pyplot as plt

# Carregue o shapefile dos estados brasileiros
shapefile = 'caminho_para_seu_shapefile/estados_do_brasil.shp'
gdf = gpd.read_file(shapefile)

# Mapeie as regiões para as cores
regioes = {
    'Norte': 'blue',
    'Nordeste': 'green',
    'Centro-Oeste': 'red',
    'Sul': 'purple',
    'Sudeste': 'orange'
}

# Crie um dicionário que mapeia os estados para suas respectivas regiões
estados_regioes = {
    'UNIR': 'Norte',
    'UFAC': 'Norte',
    'UFMA': 'Nordeste',
    'UFC': 'Nordeste',
    # Adicione os demais estados aqui...
}

# Adicione uma nova coluna ao DataFrame com as cores das regiões
gdf['Cor_Regiao'] = gdf['Sigla'].map(lambda sigla: regioes.get(estados_regioes.get(sigla, ''), 'gray'))

# Plote o mapa
fig, ax = plt.subplots(1, 1, figsize=(12, 8))
gdf.boundary.plot(ax=ax, linewidth=1, color='k')  # Plotar fronteiras dos estados
gdf.plot(ax=ax, color=gdf['Cor_Regiao'], legend=True)  # Plotar os estados coloridos pelas regiões
ax.set_title('Mapa das Regiões Brasileiras')
plt.show()
