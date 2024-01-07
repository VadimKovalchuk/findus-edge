import json

import numpy as np


METRIC = 'metric'
VALUE = 'value'
WEIGHT = 'weight'


def convert_dict_to_array(input_dict: dict):
    # create a structured array with symbol, number, and processed result fields
    dt = np.dtype([(METRIC, 'U10'), (VALUE, 'float'), (WEIGHT, 'float')])
    array = np.array(
        [
            (metric_name, metric_data[VALUE], metric_data[WEIGHT])
            for metric_name, metric_data in input_dict['metrics'].items()
        ],
        dtype=dt)
    return array


def weight(task_dict: dict):
    metrics_array = convert_dict_to_array(task_dict)
    weighted_values = metrics_array[VALUE] * metrics_array[WEIGHT]
    rate = np.sum(weighted_values)
    return {'rate': round(rate, 2)}


def main():
    test_metrics = {
        'metrics': {
            'pe': {'value': 80, 'weight': 0.4},
            'peg': {'value': 63, 'weight': 0.313},
            'pb': {'value': 93, 'weight': 0.29},
        }
    }
    result = weight(test_metrics)
    print(result)


if __name__ == '__main__':
    main()
