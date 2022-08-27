"""Functions in this module should be considered experimental, meaning there might be breaking API changes in the
future.
"""

from typing import Union, List, Optional, Callable

import numpy as np
from numpy.matlib import repmat

from dowhy.gcm.util.general import shape_into_2d


def quantile_based_fwer(p_values: Union[np.ndarray, List[float]],
                        p_values_scaling: Optional[np.ndarray] = None,
                        quantile: float = 0.5) -> float:
    """Applies a quantile based family wise error rate (FWER) control to the given p-values. This is based on the
    approach described in:

    Meinshausen, N., Meier, L. and Buehlmann, P. (2009).
    p-values for high-dimensional regression. J. Amer. Statist. Assoc.104 1671–1681

    :param p_values: A list or array of p-values.
    :param p_values_scaling: An optional list of scaling factors for each p-value.
    :param quantile: The quantile used for the p-value adjustment. By default, this is the median (0.5).
    :return: The p-value that lies on the quantile threshold. Note that this is the quantile based on scaled values
             p_values / quantile.
    """

    if quantile <= 0 or abs(quantile - 1) >= 1:
        raise ValueError("The given quantile is %f, but it needs to be on (0, 1]!" % quantile)

    p_values = np.array(p_values)
    if p_values_scaling is None:
        p_values_scaling = np.ones(p_values.shape[0])

    if p_values.shape != p_values_scaling.shape:
        raise ValueError("The p-value scaling array needs to have the same dimension as the given p-values.")

    p_values_scaling = p_values_scaling[~np.isnan(p_values)]
    p_values = p_values[~np.isnan(p_values)]

    p_values = p_values * p_values_scaling
    p_values[p_values > 1] = 1.0

    if p_values.shape[0] == 1:
        return float(p_values[0])
    else:
        return float(min(1.0, np.quantile(p_values / quantile, quantile)))


def marginal_expectation(prediction_method: Callable[[np.ndarray], np.ndarray],
                         feature_samples: np.ndarray,
                         samples_of_interest: np.ndarray,
                         features_of_interest_indices: List[int],
                         return_averaged_results: bool = True,
                         feature_perturbation: str = 'randomize_columns_jointly',
                         max_batch_size: int = -1) -> np.ndarray:
    """ Estimates the marginal expectation for samples in samples_of_interest when randomizing features that are not
    part of features_of_interest_indices. This is, this function estimates
        y^i = E[Y | do(x^i_s)] := \\int_x_s' E[Y | x^i_s, x_s'] p(x_s') d x_s',
    where x^i_s is the i-th sample from samples_of_interest, s denotes the features_of_interest_indices and
    x_s' ~ X_s' denotes the randomized features that are not in s. For an approximation of the integral, the given
    prediction_method is evaluated multiple times for the same x^i_s, but different x_s' ~ X_s'.

    :param prediction_method: Prediction method of interest. This should expect a numpy array as input for making
    predictions.
    :param feature_samples: Samples from the joint distribution. These are used as 'background samples'.
    :param samples_of_interest: Samples for which the marginal expectation should be estimated.
    :param features_of_interest_indices: Column indices of the features in s.
    :param return_averaged_results: If set to True, the expectation over all evaluated samples for the i-th
    sample_of_interest is returned. If set to False, all corresponding results for the i-th sample are returned.
    :param feature_perturbation: Type of feature permutation:
        'randomize_columns_independently': Each feature not in s is randomly permuted separately.
        'randomize_columns_jointly': All features not in s are jointly permuted. Note that this still represents an
        interventional distribution.
    :param max_batch_size: Maximum batch size for a estimating the predictions. This has a significant influence on the
    overall memory usage. If set to -1, all samples are used in one batch.
    :return: If return_averaged_results is False, a numpy array where the i-th entry belongs to the marginal expectation
    of x^i_s when randomizing the remaining features.
    If return_averaged_results is True, a two dimensional numpy array where the i-th entry contains all
    predictions for x^i_s when randomizing the remaining features.
    """
    feature_samples, samples_of_interest = shape_into_2d(feature_samples, samples_of_interest)

    batch_size = samples_of_interest.shape[0] if max_batch_size == -1 else max_batch_size
    result = [np.nan] * samples_of_interest.shape[0]

    # Make copy to avoid manipulating the original matrix.
    feature_samples = np.array(feature_samples)

    features_to_randomize = np.delete(np.arange(0, feature_samples.shape[1]), features_of_interest_indices)

    if feature_perturbation == 'randomize_columns_independently':
        feature_samples = permute_features(feature_samples, features_to_randomize, False)
    elif feature_perturbation == 'randomize_columns_jointly':
        feature_samples = permute_features(feature_samples, features_to_randomize, True)
    else:
        raise ValueError("Unknown argument %s as feature_perturbation type!" % feature_perturbation)

    # The given prediction method has to be evaluated multiple times on a large amount of different inputs. Typically,
    # the batch evaluation of a prediction model on multiple inputs at the same time is significantly faster
    # than evaluating it on single simples in a for-loop. To make use of this, we try to evaluate as many samples as
    # possible in one batch call of the prediction method. However, this also requires a lot of memory for many samples.
    # To overcome potential memory issues, multiple batch calls are performed, each with at most batch_size many
    # samples. The number of samples that are evaluated is normally
    # samples_of_interest.shape[0] * feature_samples.shape[0]. Here, we reduce it to
    # batch_size * feature_samples.shape[0]. If the batch_size would be set 1, then each samples_of_interest is
    # evaluated one by one in a for-loop.
    inputs = repmat(feature_samples, batch_size, 1)
    for offset in range(0, samples_of_interest.shape[0], batch_size):
        # Each batch consist of at most batch_size * feature_samples.shape[0] many samples. If there are multiple
        # batches, the offset indicates the index of the current samples_of_interest that has not been evaluated yet.
        if offset + batch_size > samples_of_interest.shape[0]:
            # If the batch size would be larger than the remaining amount of samples, it is reduced to only include the
            # remaining samples_of_interest.
            adjusted_batch_size = samples_of_interest.shape[0] - offset
            inputs = inputs[:adjusted_batch_size * feature_samples.shape[0]]
        else:
            adjusted_batch_size = batch_size

        for index in range(adjusted_batch_size):
            # The inputs consist of batch_size many copies of feature_samples. Here, we set the columns of the features
            # in features_of_interest_indices to their respective values in samples_of_interest.
            inputs[index * feature_samples.shape[0]:(index + 1) * feature_samples.shape[0],
            features_of_interest_indices] = samples_of_interest[offset + index, features_of_interest_indices]

        # After creating the (potentially large) input data matrix, we can evaluate the prediction method.
        predictions = np.array(prediction_method(inputs))

        for index in range(adjusted_batch_size):
            # Here, offset + index now indicates the sample index in samples_of_interest.
            if return_averaged_results:
                # This would average all prediction results obtained for the 'offset + index'-th sample in
                # samples_of_interest. This is, y^(offset + index) = E[Y | do(x^(offset + index)_s)].
                result[offset + index] = np.mean(predictions[index * feature_samples.shape[0]:
                                                             (index + 1) * feature_samples.shape[0]], axis=0)
            else:
                # This would return all prediction results obtained for the 'offset + index'-th sample in
                # samples_of_interest, i.e. the results are not averaged.
                result[offset + index] = predictions[index * feature_samples.shape[0]:
                                                     (index + 1) * feature_samples.shape[0]]

    return np.array(result)


def permute_features(feature_samples: np.ndarray,
                     features_to_permute: Union[List[int], np.ndarray],
                     randomize_features_jointly: bool) -> np.ndarray:
    # Making copy to ensure that the original object is not modified.
    feature_samples = np.array(feature_samples)

    if randomize_features_jointly:
        # Permute samples jointly. This still represents an interventional distribution.
        feature_samples[:, features_to_permute] \
            = feature_samples[np.random.choice(feature_samples.shape[0],
                                               feature_samples.shape[0],
                                               replace=False)][:, features_to_permute]
    else:
        # Permute samples independently.
        for feature in features_to_permute:
            np.random.shuffle(feature_samples[:, feature])

    return feature_samples
