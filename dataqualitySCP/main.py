import argparse
import os


def parse_input():

    parser = argparse.ArgumentParser(
            description='Evaluation and Offset prediction of the Solar Cooling Plant (SCP) sensors'
    )

    parser.add_argument(
            '--data-set-prediction',
            default=0,
            dest='data_set_prediction',
            help=f'Indicate if you want to predict a data set.',
            action="store_true"
        )

    parser.add_argument(
            '--data-set-root',
            dest='data_set_root',
            help=f'Path to the file containing the data.',
            required=False
        )

    parser.add_argument(
            '--outputs-path',
            dest='outputs_path',
            help=f'Path to the output folder.',
            required=False
        )

    parser.add_argument(
            '--simple-input-prediction',
            default=0,
            dest='simple_input_prediction',
            help=f'Indicate if you want to predict a simple sensors input.',
            action="store_true"
        )

    parser.add_argument(
            '--irr',
            dest='irr',
            type=float, 
            help=f'Irradiance sensor value.',
            required=False
        )

    parser.add_argument(
            '--flow',
            dest='flow',
            type=float,
            help=f'Flow sensor value.',
            required=False
        )

    parser.add_argument(
            '--tamb',
            dest='tamb',
            type=float,
            help=f'Ambient temperature sensor value.',
            required=False
        )

    parser.add_argument(
            '--tin',
            dest='tin',
            type=float,
            help=f'Inlet temperature sensor value.',
            required=False
        )

    parser.add_argument(
            '--tout',
            dest='tout',
            type=float,
            help=f'Outlet temperature sensor value.',
            required=False
        )

    args = parser.parse_args()

    data_set_prediction = args.data_set_prediction
    simple_input_prediction = args.simple_input_prediction
    
    assert int(data_set_prediction) + int(simple_input_prediction) == 1, \
        "[ERROR] An option --data-set-prediction or --simple-input-prediction must be specified"

    if data_set_prediction:
        data_set_root = args.data_set_root
        outputs_path = args.outputs_path

        assert data_set_root != None and outputs_path != None, \
            f'[ERROR]: "--data-set-root" and "--outputs-path" arguments must be specified."'

        assert os.path.isfile(data_set_root), \
            f'[ERROR]: Data set file not found at "{data_set_root}"'

        assert os.path.isdir(outputs_path), \
            f'[ERROR]: Directory not found at "{outputs_path}"'

        #TODO
        makepredictions_dataset(data_set_root, outputs_path)
    else:
        try:
            irr = float(args.irr)
            flow = float(args.flow)
            tamb = float(args.tamb)
            tin = float(args.tin)
            tout = float(args.tout)
        except:
            print('[ERROR]: "--irr", "--flow", "--tamb", "--tin" and "--tout" arguments must be specified as float values.')
            exit(1)

        assert irr and flow and tamb and tin and tout, \
            f'"--irr", "--flow", "--tamb", "--tin" and "--tout" arguments must be specified as float values.'

        #TODO
        makepredictions_simple(irr, flow, tamb, tin, tout)


def makepredictions_dataset(dataset_root, outputs_path):
    print("Arguments:")
    print("dataset_root", dataset_root)
    print("outputs_path", outputs_path)


def makepredictions_simple(irr, flow, tamb, tin, tout):
    print("Arguments:")
    print("irr", irr)
    print("flow", flow)
    print("tamb", tamb)
    print("tin", tin)
    print("tout", tout)


if __name__ == "__main__":

    parse_input()