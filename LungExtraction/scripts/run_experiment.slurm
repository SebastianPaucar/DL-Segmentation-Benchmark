#!/bin/bash
#SBATCH --job-name=interactive_gpu_job
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --account=notchpeak-shared-short
#SBATCH --partition=notchpeak-shared-short
#SBATCH --time=02:00:00
#SBATCH --gres=gpu:1
#SBATCH --output=slurm-%j.out
#SBATCH --error=slurm-%j.err

echo "Running on node: $(hostname)"
echo "Allocated GPUs: $CUDA_VISIBLE_DEVICES"

export PROJECT=/scratch/general/vast/u6059911/TecnicasFisicas/
export PYTHONPATH=$PROJECT/LungExtraction:$PYTHONPATH
export CTLUNGSEG=$PROJECT/LungExtraction/CTLungSeg
export PYTHONPATH=$CTLUNGSEG:$PYTHONPATH
export DATASET="MONAI"

bash $PROJECT/LungExtraction/scripts/lung_extraction.sh $PROJECT/Datasets/$DATASET/INPUT $PROJECT/LungExtraction/$DATASET/OUTPUT/NRRD

bash $PROJECT/LungExtraction/scripts/convert_nrrd_nii.sh $PROJECT/LungExtraction/$DATASET/OUTPUT/NRRD $PROJECT/LungExtraction/$DATASET/OUTPUT/NIFTI
