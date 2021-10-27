import argparse
import os
import time

from .__init__ import KEYS, __exe__, process_dataset


def parse_input():

    parser = argparse.ArgumentParser(
            description='Evaluation and Offset prediction of the Solar Cooling Plant (SCP) sensors'
    )

    parser.add_argument(
            '--default-validation',
            default=0,
            dest='default_validation',
            help=f'Validates default data set.',
            action="store_true"
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

    default_validation = args.default_validation
    data_set_prediction = args.data_set_prediction
    simple_input_prediction = args.simple_input_prediction
    
    assert int(data_set_prediction) + int(simple_input_prediction) + int(default_validation) == 1, \
        "[ERROR] An option --default-validation, --data-set-prediction or --simple-input-prediction must be specified"

    if default_validation:
        outputs_path = args.outputs_path

        assert outputs_path != None, \
            f'[ERROR]: "--outputs-path" argument must be specified.'

        assert os.path.isdir(outputs_path), \
            f'[ERROR]: Directory not found at "{outputs_path}"'

        return "default", outputs_path

    elif data_set_prediction:
        data_set_root = args.data_set_root
        outputs_path = args.outputs_path

        assert data_set_root != None and outputs_path != None, \
            f'[ERROR]: "--data-set-root" and "--outputs-path" arguments must be specified."'

        assert os.path.isfile(data_set_root), \
            f'[ERROR]: Data set file not found at "{data_set_root}"'

        assert data_set_root.endswith(".csv") or data_set_root.endswith(".xlsx"), \
            f'[ERROR]: The Data set file should have ".csv" or ".xlsx" format'

        assert os.path.isdir(outputs_path), \
            f'[ERROR]: Directory not found at "{outputs_path}"'

        return "dataset", [data_set_root, outputs_path]

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

        return "simple", [irr, flow, tamb, tin, tout]


if __name__ == "__main__":

    option, args = parse_input()

    t0 = time.time()

    if option == "default":
        process_dataset(args)    
    
    elif option == "simple":
        input = {k: [v] for k, v in zip(KEYS, args)}
        __exe__(input, verbose=True)    
    
    else: 
        dataset_root, outputs_path = args
        process_dataset(outputs_path, dataset_root)

    tf = time.time()-t0
    print(f"**Computing Time: {tf} seconds.")
