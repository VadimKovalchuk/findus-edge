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


def calculate_minmax_parameters(array: np.array):
    """
    Function to calculate Min-Max scaling parameters

    Parameters:
    array (numpy array): Input data

    Returns: {"min": value, "max": value}
    """
    min_val = np.min(array[INPUT])
    max_val = np.max(array[INPUT])
    return {"min": min_val, "max": max_val}


def apply_minmax(array: np.array, parameters: dict):
    """
    Function to apply Min-Max scaling parameters to the dataset array

    Parameters:
    parameters: {"min": value, "max": value}
    array (numpy array): Input data

    Returns: {"min": value, "max": value}
    """
    min_val = parameters["min"]
    max_val = parameters["max"]
    array[RESULT] = (array[INPUT] - min_val) / (max_val - min_val)
    return array


def apply_minmax_inverted(array: np.array, parameters: dict):
    """
    Function to apply Min-Max scaling on the input data

    Parameters:
    array (numpy array): Input data

    Returns:
    numpy array: Min-Max scaled data
    """
    minmax_norm(array, parameters)
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


calculation_func_map = {
    "minmax": calculate_minmax_parameters,
    "minmax_inverted": calculate_minmax_parameters,
    "z_score": None,
    "robust": None
}


def _read_input_from_csv(file_name: str):
    result = {}
    with open(file_name, 'r') as filehandle:
        lines = filehandle.readlines()
        for line in lines:
            symbol, value = line.split(',')
            result[symbol] = float(value)
    return result


def filter_outliers_by_boundaries(array, bottom=None, top=None):
    if top is not None and bottom is not None:
        return array[(array[INPUT] >= bottom) & (array[INPUT] <= top)]
    elif bottom is not None:
        return array[array[INPUT] >= bottom]
    elif top is not None:
        return array[array[INPUT] <= top]
    else:
        return array


def calculate_method_params(task_dict: dict):
    """
    task_dict = {
        "input_data": [{"symbol": input_value},],
        "norm_method": "minmax",
        "limits", {"top": value, "bottom": value}
        "parameters": {"method_param1_name": "method_param1_value", "method_param2_name": "param2_value"}
    }
    """
    normalization_method = task_dict['norm_method']
    input_array = convert_dict_to_array(task_dict["input_data"])
    limits: dict = task_dict["limits"]
    ref_array = filter_outliers_by_boundaries(input_array, limits.get("bottom"), limits.get("top"))
    if not task_dict.get("parameters"):
        task_dict["parameters"] = calculation_func_map[normalization_method](ref_array)



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
