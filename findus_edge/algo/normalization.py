from typing import Union

import numpy as np
import matplotlib.pyplot as plt

SYMBOL = 'symbol'
INPUT = 'input'
RESULT = 'result'


def convert_dict_to_array(input_dict: dict):
    # create a list of symbols
    symbols = list(input_dict.keys())

    # create a structured array with symbol, number, and processed result fields
    dt = np.dtype([(SYMBOL, 'U10'), (INPUT, 'float'), (RESULT, 'float')])
    array = np.zeros(len(symbols), dtype=dt)

    # fill the array with symbol and number data
    array[SYMBOL] = symbols
    array[INPUT] = list(input_dict.values())
    return array


def zscore_norm(array: np.array):
    """
    Function to apply Z-score normalization on the input data

    Parameters:
    data (numpy array): Input data

    Returns:
    numpy array: Z-score normalized data
    """
    mean = np.mean(array[INPUT])
    std = np.std(array[INPUT])
    array[RESULT] = (array[INPUT] - mean) / std
    return array


def minmax_norm(array: np.array):
    """
    Function to apply Min-Max scaling on the input data

    Parameters:
    array (numpy array): Input data

    Returns:
    numpy array: Min-Max scaled data
    """
    min_val = np.min(array[INPUT])
    max_val = np.max(array[INPUT])
    array[RESULT] = (array[INPUT] - min_val) / (max_val - min_val)
    return array


def minmax_norm_inverted(array: np.array):
    """
    Function to apply Min-Max scaling on the input data

    Parameters:
    array (numpy array): Input data

    Returns:
    numpy array: Min-Max scaled data
    """
    minmax_norm(array)
    array[RESULT] = 1.0 - array[RESULT]
    return array


def robust_norm(array: np.array):
    """
    Function to apply Robust scaling on the input data

    Parameters:
    data (numpy array): Input data

    Returns:
    numpy array: Robust scaled data
    """
    median = np.median(array[INPUT])
    q1 = np.percentile(array[INPUT], 25)
    q3 = np.percentile(array[INPUT], 75)
    iqr = q3 - q1
    array[RESULT] = (array[INPUT] - median) / iqr
    return array


def _read_input_from_csv(file_name: str):
    result = {}
    with open(file_name, 'r') as filehandle:
        lines = filehandle.readlines()
        for line in lines:
            symbol, value = line.split(',')
            result[symbol] = float(value)
    return result


def filter_outliers_by_boundaries(array, bottom=None, top=None):
    # if bottom is not None:
    #     pass
    # elif top is not None:
    #     pass
    # elif top is not None and bottom is not None:
    return array[(array[INPUT] >= bottom) & (array[INPUT] <= top)]


def plot(data):
    plt.hist(data, bins=10)
    plt.savefig('pic.png')

def main():
    input_dict = _read_input_from_csv('pe.txt')
    array = convert_dict_to_array(input_dict)
    for symbol, value in input_dict.items():
        array_value = array[array[SYMBOL] == symbol][INPUT][0]
        assert value == array_value, f"{symbol}: {value} == {array_value}"
    print('pass')
    reference_scope: np.array = filter_outliers_by_boundaries(array, bottom=0, top=80)
    minmax_norm_inverted(reference_scope)
    #robust_norm(reference_scope)
    #zscore_norm(reference_scope)
    # z_scope = reference_scope.copy()
    # z_scope[INPUT] = np.absolute(z_scope[RESULT])
    # minmax_norm_inverted(z_scope)

    plot(reference_scope[RESULT])
    print(reference_scope[RESULT])
    print((np.max(reference_scope[RESULT]), np.min(reference_scope[RESULT])))
    print((np.max(reference_scope[INPUT]), np.min(reference_scope[INPUT])))


if __name__ == '__main__':
    main()
