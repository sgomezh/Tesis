"""Functions in this module should be considered experimental, meaning there might be breaking API changes in the
future.
"""

from typing import Optional, List, Callable

import numpy as np
from sklearn.kernel_approximation import Nystroem
from sklearn.metrics import euclidean_distances

from dowhy.gcm.util.general import shape_into_2d, is_categorical


def apply_rbf_kernel(X: np.ndarray,
                     precision: Optional[float] = None) -> np.ndarray:
    """
    Estimates the RBF (Gaussian) kernel for the given input data.

    :param X: Input data.
    :param precision: Specific precision matrix for the RBF kernel. If None is given, this is inferred from the data.
    :return: The outcome of applying a RBF (Gaussian) kernel on the data.
    """
    X = shape_into_2d(X)

    distance_matrix = euclidean_distances(X, squared=True)

    if precision is None:
        precision = _median_based_precision(X)

    return np.exp(-precision * distance_matrix)


def apply_delta_kernel(X: np.ndarray) -> np.ndarray:
    """Applies the delta kernel, i.e. the distance is 1 if two entries are equal and 0 otherwise.

    :param X: Input data.
    :return: The outcome of the delta-kernel, a binary distance matrix.
    """
    X = shape_into_2d(X)
    return np.array(list(map(lambda value: value == X, X))).reshape(X.shape[0], X.shape[0]).astype(np.float)


def approximate_rbf_kernel_features(X: np.ndarray,
                                    num_random_components: int,
                                    precision: Optional[float] = None) -> np.ndarray:
    """Applies the Nystroem method to create a NxD (D << N) approximated RBF kernel map using a subset of the data,
    where N is the number of samples in X and D the number of components.

    :param X: Input data.
    :param num_random_components: Number of components D for the approximated kernel map.
    :param precision: Specific precision matrix for the RBF kernel. If None is given, this is inferred from the data.
    :return: A NxD approximated RBF kernel map, where N is the number of samples in X and D the number of components.
    """
    X = shape_into_2d(X)

    if precision is None:
        precision = _median_based_precision(X)

    return Nystroem(kernel='rbf', gamma=precision, n_components=num_random_components).fit_transform(X)


def approximate_delta_kernel_features(X: np.ndarray, num_random_components: int) -> np.ndarray:
    """Applies the Nystroem method to create a NxD (D << N) approximated delta kernel map using a subset of the data,
    where N is the number of samples in X and D the number of components. The delta kernel gives 1 if two entries are
    equal and 0 otherwise.

    :param X: Input data.
    :param num_random_components: Number of components D for the approximated kernel map.
    :return: A NxD approximated RBF kernel map, where N is the number of samples in X and D the number of components.
    """
    X = shape_into_2d(X)

    def delta_function(x, y) -> float:
        return float(x == y)

    for i, unique_element in enumerate(np.unique(X)):
        X[X == unique_element] = i

    result = Nystroem(kernel=delta_function, n_components=num_random_components).fit_transform(X.astype(int))
    result[result != 0] = 1

    return result


def auto_create_list_of_kernels(X: np.ndarray) -> List[Callable[[np.ndarray], np.ndarray]]:
    X = shape_into_2d(X)

    tmp_list = []
    for i in range(X.shape[1]):
        if not is_categorical(X[:, i]):
            tmp_list.append(apply_rbf_kernel)
        else:
            tmp_list.append(apply_delta_kernel)

    return tmp_list


def auto_create_list_of_kernel_approximations(X: np.ndarray) -> List[Callable[[np.ndarray, int], np.ndarray]]:
    X = shape_into_2d(X)

    tmp_list = []
    for i in range(X.shape[1]):
        if not is_categorical(X[:, i]):
            tmp_list.append(approximate_rbf_kernel_features)
        else:
            tmp_list.append(approximate_delta_kernel_features)

    return tmp_list


def _median_based_precision(X: np.ndarray) -> float:
    tmp = np.sqrt(euclidean_distances(X, squared=True))
    tmp = tmp - np.tril(tmp, -1)
    tmp = tmp.reshape(-1, 1)

    return 1 / np.median(tmp[tmp > 0])
