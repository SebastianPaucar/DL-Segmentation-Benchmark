import os
import pandas as pd
from scipy.stats import friedmanchisquare

# Define la ruta absoluta del directorio donde se encuentran los archivos CSV
directory = '/scratch/general/vast/u6059911/WILCOXON/RESULTS/LUNG_MONAI_ALL'  # Modifica esta línea con la ruta deseada

# Verificar si la ruta existe
if not os.path.isdir(directory):
    raise ValueError(f"La ruta proporcionada '{directory}' no es válida.")

# Encuentra todos los archivos CSV en el directorio especificado
csv_files = [f for f in os.listdir(directory) if f.endswith('.csv')]

if not csv_files:
    raise ValueError(f"No se encontraron archivos CSV en el directorio '{directory}'.")

dataframes = {}

# Cargar datos y extraer casos comunes
common_cases = None
for file in csv_files:
    file_path = os.path.join(directory, file)
    df = pd.read_csv(file_path)
    
    # Reemplazar NaN por 0 en todas las columnas numéricas
    df = df.fillna(0)
    
    if 'case' not in df.columns:
        raise ValueError(f"El archivo {file} no contiene una columna 'case'.")
    dataframes[file] = df
    if common_cases is None:
        common_cases = set(df['case'])
    else:
        common_cases &= set(df['case'])

if not common_cases:
    raise ValueError("No hay casos comunes entre los archivos CSV.")

# Filtrar los DataFrames para que solo incluyan casos comunes
for file in dataframes:
    dataframes[file] = dataframes[file][dataframes[file]['case'].isin(common_cases)]

# Verificar que las columnas de métricas coincidan (excluyendo 'case')
metric_columns = None
for file, df in dataframes.items():
    columns = list(df.columns)
    columns.remove('case')
    if metric_columns is None:
        metric_columns = columns
    elif metric_columns != columns:
        raise ValueError("Los archivos no tienen las mismas columnas de métricas.")

# Realizar la prueba de Friedman para cada métrica
results = []
for metric in metric_columns:
    print(f"Procesando métrica: {metric}")  
    metric_data = []
    for file, df in dataframes.items():
        print(f"Archivo: {file}")
        metric_data.append(df[metric].values)
        print(df[['case', metric]].head()) 
    # Realizar la prueba de Friedman
    stat, p_value = friedmanchisquare(*metric_data)
    results.append({"Métrica": metric, "Estadístico": stat, "Valor p": p_value})

# Guardar los resultados en un archivo CSV
results_df = pd.DataFrame(results)
results_df.to_csv('GENERAL_WILCOXON_TEST_LUNG_MONAI_ALL.csv', index=False)

print("Prueba de Friedman completada. Resultados guardados en 'friedman_test_LUNG_BIONDI_ALL.csv'.")

