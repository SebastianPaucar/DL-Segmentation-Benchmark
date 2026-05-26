import os
import nibabel as nib
import numpy as np
import argparse
import csv

def verify_dimensions(pred_img, gt_img):
    #Verificando dimensiones
    return pred_img.shape == gt_img.shape

def verify_affinity(pred_img, gt_img):
    #Verificando si matrices de afinidad (espacio físico) coinciden
    return np.allclose(pred_img.affine, gt_img.affine)

def calc_metrics(pred_data, gt_data):

    # Definir las clases de interés (opcionalmente puedes calcular métricas por clase)
    clases = np.unique(gt_data)

    # Calcular valores agregados de TP, TN, FP, FN
    tp = np.sum((pred_data == 1) & (gt_data == 1))  # True Positives
    tn = np.sum((pred_data == 0) & (gt_data == 0))  # True Negatives
    fp = np.sum((pred_data == 1) & (gt_data == 0))  # False Positives
    fn = np.sum((pred_data == 0) & (gt_data == 1))  # False Negatives

    # Calcular Pixel-Wise Accuracy
    voxel_correctos = tp + tn
    total_voxeles = tp + tn + fp + fn
    pixel_wise_accuracy = voxel_correctos / total_voxeles

    # Calcular Pixel-Wise Precision
    voxeles_positivos = tp + fp
    pixel_wise_precision = tp / voxeles_positivos

    # Calcular IoU por clase
    ious_por_clase = {}
    for clase in clases:
        interseccion = np.sum((pred_data == clase) & (gt_data == clase))
        union = np.sum((pred_data == clase) | (gt_data == clase))
        iou_clase = interseccion / union if union != 0 else 0
        ious_por_clase[clase] = iou_clase

    return pixel_wise_accuracy, pixel_wise_precision, ious_por_clase, tp, tn, fp, fn

def save_results(output_folder, resultados):
    
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, "metrics_results.csv")
    
    # Clases del IoU
    clases = sorted(set(clase for _, _, ious_por_clase, _, _, _, _ in resultados for clase in ious_por_clase))
    
    # Create CSV
    with open(output_path, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        # Encabezado
        header = ["File", "Pixel-Wise Accuracy", "Pixel-Wise Precision", "TP", "TN", "FP", "FN"] + [f"IoU_clase_{clase}" for clase in clases]
        writer.writerow(header)
        
        # Datos
        for pred_file, pixel_wise_accuracy, pixel_wise_precision, ious_por_clase, tp, tn, fp, fn in resultados:
            # Crear la fila con los valores básicos y las métricas por clase
            row = [pred_file, pixel_wise_accuracy, pixel_wise_precision, tp, tn, fp, fn] + [ious_por_clase.get(clase, "") for clase in clases]
            writer.writerow(row)
    
    print(f"Metrics saved in {output_path}")

def process_folders(pred_folder, gt_folder, output_folder):
    archivos_pred = sorted([f for f in os.listdir(pred_folder) if f.endswith('_seg.nii.gz')])
    print(archivos_pred)
    archivos_gt = sorted([f for f in os.listdir(gt_folder) if f.endswith('_gt.nii.gz')])
    print(archivos_gt)

    # Comprobamos que ambas carpetas tengan el mismo número de archivos
    if len(archivos_pred) != len(archivos_gt):
        print("Error: The folders do not contain the same number of .nii files.")
        return
    
    results = []

    # Procesar cada archivo de predicción y ground truth
    for pred_file, gt_file in zip(archivos_pred, archivos_gt):
        pred_path = os.path.join(pred_folder, pred_file)
        gt_path = os.path.join(gt_folder, gt_file)

        # Cargar las imágenes NIfTI
        pred_img = nib.load(pred_path)
        gt_img = nib.load(gt_path)

        # Verificar dimensiones y afinidad
        if verify_dimensions(pred_img, gt_img) and verify_affinity(pred_img, gt_img):
            pred_data = pred_img.get_fdata()
            gt_data = gt_img.get_fdata()

            pixel_wise_accuracy, pixel_wise_precision, ious_por_clase, tp, tn, fp, fn = calc_metrics(pred_data, gt_data)
            results.append((pred_file, pixel_wise_accuracy, pixel_wise_precision, ious_por_clase, tp, tn, fp, fn))

            print(f"File: {pred_file}")
            print(f"  Pixel-Wise Accuracy: {pixel_wise_accuracy:.4f}")
            print(f"  Pixel-Wise Precision: {pixel_wise_precision:.4f}")
            for clase, iou in ious_por_clase.items():
                print(f"  IoU for class {clase}: {iou:.4f}")
            print("TP:",tp,"TN:",tn,"FP:",fp,"FN:", fn)
        
        else:
            print(f"Error: Dimensions or spatial alignment do not match for {pred_file} y {gt_file}")

    # Guardar los resultados en la carpeta de salida
    save_results(output_folder, results)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-pred_folder", type=str, help="Pred folder path")
    parser.add_argument("-gt_folder", type=str, help="Ground truth folder path")
    parser.add_argument("-output_folder", type=str, help="Output folder path")

    args = parser.parse_args()

    process_folders(args.pred_folder, args.gt_folder, args.output_folder)

