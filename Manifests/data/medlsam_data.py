import os

def generate_txt_files(image_dir, label_dir, output_dir, support_count):
    """
    Genera archivos .txt para los conjuntos support y query.

    Args:
        image_dir (str): Directorio de las imágenes.
        label_dir (str): Directorio de las etiquetas.
        output_dir (str): Directorio donde se guardarán los archivos .txt.
        support_count (int): Número de imágenes a incluir en el conjunto support.
    """
    # Crear el directorio de salida si no existe
    os.makedirs(output_dir, exist_ok=True)

    # Obtener todos los archivos del directorio de imágenes
    file_names = sorted([f for f in os.listdir(image_dir) if f.endswith(".nii.gz")])

    if len(file_names) < support_count:
        raise ValueError("El número de archivos es menor que el número de support especificado.")

    # Dividir archivos en support y query
    support_files = file_names[:support_count]
    query_files = file_names[support_count:]

    # Crear listas de rutas completas
    support_images = [os.path.join(image_dir, f) for f in support_files]
    support_labels = [os.path.join(label_dir, f) for f in support_files]
    query_images = [os.path.join(image_dir, f) for f in query_files]
    query_labels = [os.path.join(label_dir, f) for f in query_files]

    # Guardar las listas en archivos .txt
    def save_list(file_path, data_list):
        with open(file_path, "w") as f:
            f.write("\n".join(data_list))

    save_list(os.path.join(output_dir, "support_image.txt"), support_images)
    save_list(os.path.join(output_dir, "support_label.txt"), support_labels)
    save_list(os.path.join(output_dir, "query_image.txt"), query_images)
    save_list(os.path.join(output_dir, "query_label.txt"), query_labels)

    print(f"Archivos .txt generados en {output_dir}.")

# Parámetros generales
image_dir = "/scratch/general/vast/u6059911/datasets/LUNG_NII_MONAI_MEDLSAM/dir_5"
label_dir = "/scratch/general/vast/u6059911/datasets/MONAI/GROUND_TRUTH"
output_dir = "/scratch/general/vast/u6059911/models/MedLSAM/config/data/MONAI_LUNG_dir_5"  # Cambia este directorio si lo necesitas
support_count = 9  # Número de imágenes para el conjunto support

# Llamar a la función
generate_txt_files(image_dir, label_dir, output_dir, support_count)

