from typing import Union

import numpy as np

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


def zscore_norm(data):
    """
    Function to apply Z-score normalization on the input data

    Parameters:
    data (numpy array): Input data

    Returns:
    numpy array: Z-score normalized data
    """
    mean = np.mean(data)
    std = np.std(data)
    zscore = (data - mean) / std
    return zscore


def minmax_norm(array: np.array, custom_max: Union[None, float] = None, custom_min: Union[None, float] = None):
    """
    Function to apply Min-Max scaling on the input data

    Parameters:
    array (numpy array): Input data

    Returns:
    numpy array: Min-Max scaled data
    """
    min_val = custom_min if custom_min is not None else np.min(array[INPUT])
    max_val = custom_max if custom_max is not None else np.max(array[INPUT])
    array[RESULT] = (array[INPUT] - min_val) / (max_val - min_val)
    return array


def minmax_norm_inverted(array: np.array, custom_max: Union[None, float] = None, custom_min: Union[None, float] = None):
    """
    Function to apply Min-Max scaling on the input data

    Parameters:
    array (numpy array): Input data

    Returns:
    numpy array: Min-Max scaled data
    """
    minmax_norm(array, custom_max, custom_min)
    array[RESULT] = 1.0 - array[RESULT]
    return array


def robust_norm(data):
    """
    Function to apply Robust scaling on the input data

    Parameters:
    data (numpy array): Input data

    Returns:
    numpy array: Robust scaled data
    """
    median = np.median(data)
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    robust = (data - median) / iqr
    return robust


def _read_input_from_csv(file_name: str):
    result = {}
    with open(file_name, 'r') as filehandle:
        lines = filehandle.readlines()
        for line in lines:
            symbol, value = line.split(',')
            result[symbol] = float(value)
    return result


def main():
    input_dict = _read_input_from_csv('pe.txt')
    array = convert_dict_to_array(input_dict)
    for symbol, value in input_dict.items():
        array_value = array[array[SYMBOL] == symbol][INPUT][0]
        assert value == array_value, f"{symbol}: {value} == {array_value}"
    print('pass')
    result = minmax_norm_inverted(array, custom_max=80)
    print(array)
    print((np.max(array[INPUT]), np.min(array[INPUT])))


if __name__ == '__main__':
    main()
