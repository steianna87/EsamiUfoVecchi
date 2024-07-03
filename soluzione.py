import pandas as pd

# Percorso dei file CSV
path = 'C:/Users/work/Desktop/Ingegneria Gestionale L8 (triennale)/III anno/II semestre/Tecniche di Programmazione/DatiEsportatiInCSV/'

# Caricamento dei file CSV
sightings_df = pd.read_csv(f'{path}sighting_202407022006.csv')
neighbor_df = pd.read_csv(f'{path}neighbor_202407022006.csv')
state_df = pd.read_csv(f'{path}state_202407022007.csv')

# Mostra i primi record di ogni DataFrame
print("Sighting DataFrame:")
print(sightings_df.head())
print("\nNeighbor DataFrame:")
print(neighbor_df.head())
print("\nState DataFrame:")
print(state_df.head())

# Filtrare i dati per lo stato 'AZ' e la forma 'circle'
filtered_sightings = sightings_df[(sightings_df['state'] == 'AZ') & (sightings_df['shape'] == 'circle')]

# Mostrare i dati filtrati
print("\nFiltered Sightings DataFrame (AZ and circle):")
print(filtered_sightings.head())
print(f"Number of filtered rows: {len(filtered_sightings)}")

# Contare il numero di nodi (città con avvistamenti di forma "circle" in "AZ")
city_counts = filtered_sightings.groupby('city').size().reset_index(name='count')
num_nodi = city_counts['city'].nunique()

# Mostrare i dati di conteggio delle città
print("\nCity Counts DataFrame:")
print(city_counts.head())
print(f"Number of nodes (unique cities): {num_nodi}")

# Creare il grafo
# Contare il numero di archi (collegamenti tra città con avvistamenti della stessa forma e anno)
filtered_sightings['year'] = pd.to_datetime(filtered_sightings['datetime']).dt.year
graph_data = filtered_sightings.merge(filtered_sightings, on='year', suffixes=('_1', '_2'))
graph_data = graph_data[graph_data['city_1'] < graph_data['city_2']]
graph_data = graph_data.groupby(['city_1', 'city_2']).size().reset_index(name='weight')
num_spigoli = len(graph_data)

# Mostrare i dati del grafo
print("\nGraph Data DataFrame:")
print(graph_data.head())
print(f"Number of edges (graph data rows): {num_spigoli}")
