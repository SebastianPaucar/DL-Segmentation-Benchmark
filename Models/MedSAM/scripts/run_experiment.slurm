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
export PYTHONPATH=$PROJECT/Models:$PYTHONPATH
export MEDSAM=$PROJECT/Models/MedSAM
export PYTHONPATH=$MEDSAM:$PYTHONPATH
export DATASET="MONAI"

bash $MEDSAM/scripts/preprocessing.sh $MEDSAM/data/$DATASET/images $MEDSAM/data/$DATASET/labels $MEDSAM/data/$DATASET

bash $MEDSAM/scripts/npz.sh $MEDSAM/data/$DATASET/MedSAM_train/CT_Abd $MEDSAM/data/$DATASET/npy

bash $MEDSAM/scripts/inference_direct.sh $MEDSAM/data/$DATASET/MedSAM_train/CT_Abd $MEDSAM/preds/$DATASET/CT_Abd $MEDSAM/lite_medsam.pth $MEDSAM/preds/$DATASET/CT_Abd_overlay

bash $MEDSAM/scripts/metrics.sh $MEDSAM/preds/$DATASET/CT_Abd/CT_Abd/ $MEDSAM/data/$DATASET/MedSAM_train/CT_Abd/ $MEDSAM/data/$DATASET/Results/
