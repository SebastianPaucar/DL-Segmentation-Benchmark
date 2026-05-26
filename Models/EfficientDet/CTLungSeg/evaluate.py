import argparse
import pandas as pd
import SimpleITK as sitk

from CTLungSeg.utils import read_image

from CTLungSeg.metrics import dice
from CTLungSeg.metrics import recall
from CTLungSeg.metrics import precision
from CTLungSeg.metrics import specificity
from CTLungSeg.metrics import accuracy
from CTLungSeg.metrics import tp, tn, fp, fn

def parse_args():
    description='Script to evaluate the goodness of the segmentation against the ground truth'

    parser = argparse.ArgumentParser(description=description)

    _ = parser.add_argument('--gt',
                            dest='gt',
                            action='store',
                            type=str,
                            required=True,
                            help='Path to the ground truth image')
    
    _ = parser.add_argument('--pred',
                            dest='pred',
                            action='store',
                            type=str,
                            required=True,
                            help='Path to the predicted image to evaluate')
    
    _ = parser.add_argument('--output',
                            dest='output',
                            action='store',
                            type=str,
                            required=False,
                            default=None,
                            help='Path to the output .csv file  to store the evaluation results')
    args = parser.parse_args()

    return args


def main(ground_truth,predic_dir,ouput_csv):

    # read the images
    gt = read_image(ground_truth)
    pred = read_image(predic_dir)

    # convert to array

    gt = sitk.GetArrayFromImage(gt)
    pred = sitk.GetArrayFromImage(pred)


    # and compute all the required metrics

    metrics_dict = {
                "ground truth": [ground_truth],
                "prediction": [predic_dir],
                "dice score": [dice(gt, pred)],
                "recall": [recall(gt, pred)],
                "precision": [precision(gt, pred)],
                "specificity": [specificity(gt, pred)],
                "accuracy": [accuracy(gt, pred)],
                "tp": [tp(gt, pred)],
                "tn": [tn(gt, pred)],
                "fp": [fp(gt, pred)],
                "fn": [fn(gt, pred)]
                }
    
    # and display the metrics
    print(f'**Evaluation Results**')
    for key, val in metrics_dict.items():
        print(f'\t{key}: {val[-1]}')

    # now save the output results
    # if specified, check the output file validity
    
    if ouput_csv is not None:
        ext = ouput_csv.split('.')[-1]
        # check it is a .csv
        if ext != 'csv':
            raise ValueError(f'output file must be a .csv, received .{ext} instead')
        
        # and save the results
        df = pd.DataFrame().from_dict(metrics_dict)
        _ = df.to_csv(ouput_csv, sep=',', index=False)

if __name__ == '__main__':
    args = parse_args()
    ground_truth = args.gt
    predic_dir = args.pred
    ouput_csv = args.output
    main(ground_truth,predic_dir,ouput_csv)