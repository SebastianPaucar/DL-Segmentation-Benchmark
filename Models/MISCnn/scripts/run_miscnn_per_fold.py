import tensorflow as tf
from miscnn.data_loading.interfaces import NIFTI_interface
from miscnn import Data_IO, Preprocessor, Data_Augmentation, Neural_Network
from miscnn.processing.subfunctions import Normalization, Clipping, Resampling
from miscnn.neural_network.architecture.unet.standard import Architecture
from miscnn.neural_network.metrics import tversky_crossentropy, dice_soft, \
                                          dice_crossentropy, tversky_loss
from miscnn.evaluation.cross_validation import cross_validation
from tensorflow.keras.callbacks import ReduceLROnPlateau, TensorBoard, \
                                       EarlyStopping, CSVLogger, ModelCheckpoint
from miscnn.evaluation.cross_validation import run_fold, load_disk2fold
import argparse
import os

os.environ["CUDA_VISIBLE_DEVICES"] = ""

parser = argparse.ArgumentParser(description="Automated COVID-19 Segmentation")
parser.add_argument("-f", "--fold", help="Cross-validation fold. Range: [0:5]",
                    required=True, type=int, dest="fold")
args = parser.parse_args()
fold = args.fold

fold_subdir = os.path.join("evaluation", "fold_" + str(fold))
interface = NIFTI_interface(channels=1, classes=4)
data_io = Data_IO(interface, input_path="/scratch/general/vast/u6059911/models/covid19.MIScnn/data", delete_batchDir=False)

data_aug = Data_Augmentation(cycles=1, scaling=True, rotations=True,
                             elastic_deform=True, mirror=True,
                             brightness=True, contrast=True, gamma=True,
                             gaussian_noise=True)

sf_clipping = Clipping(min=-1250, max=250)
sf_normalize = Normalization(mode="grayscale")
sf_resample = Resampling((1.58, 1.58, 2.70))
sf_zscore = Normalization(mode="z-score")

sf = [sf_clipping, sf_normalize, sf_resample, sf_zscore]

pp = Preprocessor(data_io, data_aug=data_aug, batch_size=2, subfunctions=sf,
                  prepare_subfunctions=True, prepare_batches=False,
                  analysis="patchwise-crop", patch_shape=(160, 160, 80))

unet_standard = Architecture(depth=4, activation="softmax", batch_normalization=True)

model = Neural_Network(preprocessor=pp, architecture=unet_standard,
                       loss=tversky_crossentropy,
                       metrics=[tversky_loss, dice_soft, dice_crossentropy],
                       batch_queue_size=3, workers=3, learninig_rate=0.001)

model.load(os.path.join(fold_subdir, f"model.fold_{fold}.best_loss.hdf5"))

training, validation = load_disk2fold(os.path.join(fold_subdir, "sample_list.json"))

model.predict(validation, return_output=False)
