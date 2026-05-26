import os
import numpy as np
import nibabel as nib
import argparse

def transform_mask_directory(input_dir, output_dir):

    os.makedirs(output_dir, exist_ok=True)
    
    for filename in os.listdir(input_dir):
        if filename.endswith(".nii.gz"):
            input_file = os.path.join(input_dir, filename)
            base_name = os.path.splitext(os.path.splitext(filename)[0])[0]  
            output_file = os.path.join(output_dir, f"{base_name}_seg.nii.gz")
            
            nii = nib.load(input_file)
            mask = nii.get_fdata()
            
            if mask.shape[-1] == 1:
                mask = np.squeeze(mask, axis=-1)
            
            transformed_mask = np.where(mask == 3, 1, 0) 
            
            new_nii = nib.Nifti1Image(transformed_mask, nii.affine, nii.header)
            
            nib.save(new_nii, output_file)
            print(f"Transformado y guardado: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transforma máscaras NIfTI eliminando clases no deseadas y reduciendo dimensiones.")
    parser.add_argument("-input_directory", required=True, help="Directorio de entrada con archivos .nii.gz")
    parser.add_argument("-output_directory", required=True, help="Directorio de salida para guardar los archivos transformados")
    args = parser.parse_args()
    
    transform_mask_directory(args.input_directory, args.output_directory)
