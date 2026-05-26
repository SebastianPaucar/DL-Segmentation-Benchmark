import os
import argparse
import pandas as pd

def parse_args():
    description='Script to results'

    parser = argparse.ArgumentParser(description=description)

    _ = parser.add_argument('--path',
                            dest='path',
                            action='store',
                            type=str,
                            required=True,
                            help='Path to the csv file')
    
    _ = parser.add_argument('--output',
                            dest='output',
                            action='store',
                            type=str,
                            required=True,
                            default=None,
                            help='Path to the output .csv file  to store the evaluation results')    


    args = parser.parse_args()

    return args


def main():

    args = parse_args()

    file_dir = args.path

    contenido = os.listdir(file_dir)

    total_ds = 0.0
    total_rec = 0.0
    total_pre = 0.0
    total_spe = 0.0
    total_acc = 0.0

    cont = 0

    for file_csv in contenido:
        
        data = pd.read_csv(file_dir + file_csv)

        
        ds = data['dice score'].values
        rec = data['recall'].values
        pre = data['precision'].values
        spe = data['specificity'].values
        acc = data['accuracy'].values

        cont = cont + 1
        print("ARCHIVO N: ",cont )

        print (
                "dice score" , ds ,
                "recall",  rec ,
                "precision" , pre ,
                "specificity" , spe ,
                "accuracy" , acc , "\n"
        )

        total_ds = total_ds + ds
        total_rec = total_rec + rec
        total_pre = total_pre + pre
        total_spe = total_spe + spe
        total_acc = total_acc + acc

    print ( "TOTAL SUMA DE METRICAS:\n"
                "dice score" , total_ds ,
                "recall",  total_rec ,
                "precision" , total_pre ,
                "specificity" , total_spe ,
                "accuracy" , total_acc
        )
    
    prom_ds = total_ds/len(contenido)
    prom_rec = total_rec/len(contenido)
    prom_pre = total_pre/len(contenido)
    prom_spe = total_spe/len(contenido)
    prom_acc = total_acc/len(contenido)

    print ( "PROMEDIO DE METRICAS:\n"
                "dice score" , prom_ds ,
                "recall",  prom_rec  ,
                "precision" , prom_pre,
                "specificity" , prom_spe ,
                "accuracy" , prom_acc, "\n"
        )


    metrics_name =["dice score","recall","precision","specificity","accuracy"]
    metrics_value = [prom_ds,prom_rec,prom_pre,prom_spe,prom_acc]

    mi_CSV = {"Nombre":metrics_name,"Valor":metrics_value}
    

    # now save the output results
    # if specified, check the output file validity
    
    if args.output is not None:
        ext = args.output.split('.')[-1]
        # check it is a .csv
        if ext != 'csv':
            raise ValueError(f'output file must be a .csv, received .{ext} instead')
        
        # and save the results
        df = pd.DataFrame().from_dict(mi_CSV)
        _ = df.to_csv(args.output, sep=',', index=False)
        print("Results saved successfully in: ",args.output)


if __name__ == '__main__':

    args = parse_args()
    main()