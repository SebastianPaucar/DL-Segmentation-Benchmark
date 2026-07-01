import os

# Ruta del directorio donde se encuentran los archivos CSV
directorio = '/scratch/general/vast/u6059911/WILCOXON/RESULTS/LUNG_MONAI_ALL/monai'

# Encuentra todos los archivos CSV en el directorio
csv_files = [f for f in os.listdir(directorio) if f.endswith('.csv')]

# Reemplazar los espacios por comas en cada archivo CSV, sin afectar la primera fila
for file in csv_files:
    archivo_path = os.path.join(directorio, file)
    
    # Leer el contenido del archivo
    with open(archivo_path, 'r') as f:
        lines = f.readlines()
    
    # Procesar solo las filas a partir de la segunda (excluyendo la primera fila de encabezado)
    for i in range(1, len(lines)):
        # Reemplazar los espacios por comas en las filas de datos
        lines[i] = lines[i].replace(' ', ',')
    
    # Guardar el archivo modificado
    with open(archivo_path, 'w') as f:
        f.writelines(lines)

    print(f"Archivo {file} procesado con éxito.")
    
print("Todos los archivos CSV han sido delimitados correctamente.")

