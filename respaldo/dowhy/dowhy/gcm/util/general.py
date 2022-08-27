"""Functions in this module should be considered experimental, meaning there might be breaking API changes in the
future.
"""

import random
from typing import Union, List, Dict, Any

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from sklearn.preprocessing import OneHotEncoder


def shape_into_2d(*args):
    """If necessary, shapes the numpy inputs into 2D matrices.

    Example:
        array([1, 2, 3]) -> array([[1], [2], [3]])
        2 -> array([[2]])

    :param args: The function expects numpy arrays as inputs and returns a reshaped (2D) version of them (if necessary).
    :return: Reshaped versions of the input numpy arrays. For instance, given 1D inputs X, Y and Z, then
             shape_into_2d(X, Y, Z) reshapes them into 2D and returns them. If an input is already 2D, it will not be
             modified and returned as it is.
    """

    def shaping(X: np.ndarray):
        if X.ndim < 2:
            return np.column_stack([X])
        elif X.ndim > 2:
            raise ValueError("Cannot reshape a %dD array into a 2D array!" % X.ndim)

        return X

    result = [shaping(x) for x in args]

    if len(result) == 1:
        return result[0]
    else:
        return result


def convert_numpy_array_to_pandas_column(*args) -> Union[np.ndarray, List[np.ndarray]]:
    """Prepares given np arrays to be used as column data in a pd data frame. This means, for np arrays with
    one feature, a flatten version is returned for a better performance. For np arrays with multiple columns,
    the entries (row-wise) are returned in a list.
    Example:
       array([[1], [2]]) -> array([1, 2])
       array([[1, 2], [3, 4]]) -> list([[1, 2], [3, 4]])
       array([[1]]) -> array([1])

    :param args: The function expects numpy arrays and returns them as a list. This is equivalent to apply list(array)
                 to each input separately and converting a scalar array into a list with one element.
    :return: List versions of the input numpy arrays.
    """

    # TODO: Remove this function and refactor places where it is currently used accordingly.
    def shaping(X):
        X = X.squeeze()

        if X.ndim == 0:
            return np.array([X])

        if X.ndim > 1:
            return list(X)
        else:
            return X

    result = [shaping(x) for x in args]

    if len(result) == 1:
        return result[0]
    else:
        return result


def convert_to_data_frame(dict_with_np_arrays: Dict[Any, np.ndarray]) -> pd.DataFrame:
    return pd.DataFrame(
        {k: convert_numpy_array_to_pandas_column(v) for (k, v) in dict_with_np_arrays.items()})


def column_stack_selected_numpy_arrays(dict_with_np_arrays: Union[Dict[Any, np.ndarray], pd.DataFrame],
                                       keys: List[Any]) -> np.ndarray:
    return np.column_stack([dict_with_np_arrays[x] for x in keys])


def set_random_seed(random_seed: int) -> None:
    """Sets random seed in numpy and the random module.

    :param random_seed: Random see for the numpy and random module.
    :return: None
    """
    np.random.seed(random_seed)
    random.seed(random_seed)


def fit_one_hot_encoders(X: np.ndarray) -> Dict[int, OneHotEncoder]:
    """Fits one-hot encoders to each categorical column in X. A categorical input needs to be a string, i.e. a
    categorical column consists only of strings.

    :param X: Input data matrix.
    :return: Dictionary that maps a column index to a scikit OneHotEncoder.
    """
    X = shape_into_2d(X)

    one_hot_encoders = {}
    for column in range(X.shape[1]):
        if isinstance(X[0, column], str):
            one_hot_encoders[column] = OneHotEncoder(handle_unknown='ignore')
            one_hot_encoders[column].fit(X[:, column].reshape(-1, 1))

    return one_hot_encoders


def apply_one_hot_encoding(X: np.ndarray, one_hot_encoder_map: Dict[int, OneHotEncoder]) -> np.ndarray:
    X = shape_into_2d(X)

    if not one_hot_encoder_map:
        return X

    one_hot_features = []

    for column in range(X.shape[1]):
        if column in one_hot_encoder_map:
            one_hot_features.append(one_hot_encoder_map[column].transform(X[:, column].reshape(-1, 1)).toarray())
        else:
            one_hot_features.append(X[:, column].reshape(-1, 1))

    return np.hstack(one_hot_features).astype(float)


def is_categorical(X: np.ndarray) -> bool:
    """ Checks if all of the given columns are categorical, i.e. either a string or a boolean. Only if all of the
    columns are categorical, this method will return True. Alternatively, consider has_categorical for checking if any
    of the columns is categorical.

    Note: A np matrix with mixed data types might internally convert numeric columns to strings and vice versa. To
    ensure that the given given data keeps the original data type, consider converting/initializing it with the dtype
    'object'. For instance: np.array([[1, 'True', '0', 0.2], [3, 'False', '1', 2.3]], dtype=object)

    :param X: Input array to check if all columns are categorical.
    :return: True if all columns of the input are categorical, False otherwise.
    """
    X = shape_into_2d(X)

    status = True
    for column in range(X.shape[1]):
        if (isinstance(X[0, column], int) or isinstance(X[0, column], float)) and np.isnan(X[0, column]):
            raise ValueError("Input contains NaN values! This is currently not supported. "
                             "Consider imputing missing values.")

        status &= (isinstance(X[0, column], str) or isinstance(X[0, column], bool))

        if not status:
            break

    return status


def has_categorical(X: np.ndarray) -> bool:
    """ Checks if any of the given columns are categorical, i.e. either a string or a boolean. If any of the columns
    is categorical, this method will return True. Alternatively, consider is_categorical for checking if all columns are
    categorical.

    Note: A np matrix with mixed data types might internally convert numeric columns to strings and vice versa. To
    ensure that the given given data keeps the original data type, consider converting/initializing it with the dtype
    'object'. For instance: np.array([[1, 'True', '0', 0.2], [3, 'False', '1', 2.3]], dtype=object)

    :param X: Input array to check if all columns are categorical.
    :return: True if all columns of the input are categorical, False otherwise.
    """
    X = shape_into_2d(X)

    status = False
    for column in range(X.shape[1]):
        status |= is_categorical(X[:, column])

        if status:
            break

    return status


def means_difference(randomized_predictions: np.ndarray, baseline_values: np.ndarray) -> np.ndarray:
    return np.mean(randomized_predictions).squeeze() - np.mean(baseline_values).squeeze()


def geometric_median(x: np.ndarray) -> np.ndarray:
    def distance_function(x_input: np.ndarray) -> np.ndarray:
        return np.sum(np.sqrt(np.sum((x_input - x) ** 2, axis=1)))

    return minimize(distance_function, np.sum(x, axis=0) / x.shape[0]).x
