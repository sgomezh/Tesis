import random
from typing import List, Union

import numpy as np
import pytest
from flaky import flaky
from pytest import approx

from dowhy.gcm.shapley import estimate_shapley_values, ShapleyApproximationMethods, ShapleyConfig
from dowhy.gcm.util.general import means_difference


@pytest.fixture
def preserve_random_generator_state():
    numpy_state = np.random.get_state()
    random_state = random.getstate()
    yield
    np.random.set_state(numpy_state)
    random.setstate(random_state)


def test_given_few_features_when_estimate_shapley_values_with_auto_approx_then_returns_correct_result():
    X, coefficients = _generate_data(4)

    def model(x): return np.sum(coefficients * x, axis=1)

    shapley_values = estimate_shapley_values(
        lambda subset: _set_function_for_aggregated_feature_attribution(subset, X, model),
        X.shape[1],
        ShapleyConfig(approximation_method=ShapleyApproximationMethods.AUTO, n_jobs=1))

    assert coefficients * (X[0, :] - np.mean(X, axis=0)) == approx(shapley_values, abs=0.001)


def test_given_many_features_when_estimate_shapley_values_with_auto_approx_then_returns_correct_result():
    X, coefficients = _generate_data(15)

    def model(x): return np.sum(coefficients * x, axis=1)

    shapley_values = estimate_shapley_values(
        lambda subset: _set_function_for_aggregated_feature_attribution(subset, X, model),
        X.shape[1],
        ShapleyConfig(approximation_method=ShapleyApproximationMethods.AUTO, n_jobs=1))

    assert coefficients * (X[0, :] - np.mean(X, axis=0)) == approx(shapley_values, abs=0.001)


def test_estimate_shapley_values_symmetry_exact():
    X, coefficients = _generate_data(15)

    def model(x): return np.sum(coefficients * x, axis=1)

    shapley_values = estimate_shapley_values(
        lambda subset: _set_function_for_aggregated_feature_attribution(subset, X, model),
        X.shape[1],
        ShapleyConfig(approximation_method=ShapleyApproximationMethods.EXACT, n_jobs=1))

    assert coefficients * (X[0, :] - np.mean(X, axis=0)) == approx(shapley_values, abs=0.001)


def test_estimate_shapley_values_symmetry_exact_fast():
    X, coefficients = _generate_data(15)

    def model(x): return np.sum(coefficients * x, axis=1)

    shapley_values = estimate_shapley_values(
        lambda subset: _set_function_for_aggregated_feature_attribution(subset, X, model),
        X.shape[1],
        ShapleyConfig(approximation_method=ShapleyApproximationMethods.EXACT_FAST, n_jobs=1))

    assert coefficients * (X[0, :] - np.mean(X, axis=0)) == approx(shapley_values, abs=0.001)


def test_estimate_shapley_values_symmetry_approximation_via_subset():
    X, coefficients = _generate_data(15)

    def model(x): return np.sum(coefficients * x, axis=1)

    shapley_values = estimate_shapley_values(
        lambda subset: _set_function_for_aggregated_feature_attribution(subset, X, model),
        X.shape[1],
        ShapleyConfig(approximation_method=ShapleyApproximationMethods.SUBSET_SAMPLING))

    assert coefficients * (X[0, :] - np.mean(X, axis=0)) == approx(shapley_values, abs=0.001)


def test_evaluate_set_function_via_shapley_symmetry_approximation_via_permutation():
    X, coefficients = _generate_data(15)

    def model(x): return np.sum(coefficients * x, axis=1)

    shapley_values = estimate_shapley_values(
        lambda subset: _set_function_for_aggregated_feature_attribution(subset, X, model),
        X.shape[1],
        ShapleyConfig(approximation_method=ShapleyApproximationMethods.PERMUTATION))

    assert coefficients * (X[0, :] - np.mean(X, axis=0)) == approx(shapley_values, abs=0.001)


def test_estimate_shapley_values_symmetry_approximation_via_early_stopping():
    X, coefficients = _generate_data(15)

    def model(x): return np.sum(coefficients * x, axis=1)

    shapley_values = estimate_shapley_values(
        lambda subset: _set_function_for_aggregated_feature_attribution(subset, X, model),
        X.shape[1],
        ShapleyConfig(approximation_method=ShapleyApproximationMethods.EARLY_STOPPING))

    assert coefficients * (X[0, :] - np.mean(X, axis=0)) == approx(shapley_values, abs=0.001)


def test_estimate_shapley_values_symmetry_approximation_via_subset_with_random_seed(preserve_random_generator_state):
    X, coefficients = _generate_data(15)

    def model(x): return np.sum(coefficients * x, axis=1)

    shapley_config = ShapleyConfig(approximation_method=ShapleyApproximationMethods.SUBSET_SAMPLING)
    assert estimate_shapley_values(
        lambda subset: _set_function_for_aggregated_feature_attribution(subset, X, model),
        X.shape[1],
        shapley_config) != approx(estimate_shapley_values(
        lambda subset: _set_function_for_aggregated_feature_attribution(subset, X, model),
        X.shape[1],
        shapley_config), abs=0)

    np.random.seed(0)
    shapley_values_1 = estimate_shapley_values(
        lambda subset: _set_function_for_aggregated_feature_attribution(subset, X, model),
        X.shape[1],
        shapley_config)
    np.random.seed(0)
    shapley_values_2 = estimate_shapley_values(
        lambda subset: _set_function_for_aggregated_feature_attribution(subset, X, model),
        X.shape[1],
        shapley_config)

    assert shapley_values_1 == approx(shapley_values_2, abs=0)


@flaky(max_runs=2)
def test_estimate_shapley_values_symmetry_approximation_via_permutation_with_random_seed(
        preserve_random_generator_state):
    X, coefficients = _generate_data(15)

    def model(x): return np.sum(coefficients * x, axis=1)

    shapley_config = ShapleyConfig(approximation_method=ShapleyApproximationMethods.PERMUTATION)
    assert estimate_shapley_values(
        lambda subset: _set_function_for_aggregated_feature_attribution(subset, X, model),
        X.shape[1],
        shapley_config) != approx(
        estimate_shapley_values(
            lambda subset: _set_function_for_aggregated_feature_attribution(subset, X, model),
            X.shape[1],
            shapley_config), abs=0)

    np.random.seed(0)
    shapley_values_1 = estimate_shapley_values(
        lambda subset: _set_function_for_aggregated_feature_attribution(subset, X, model),
        X.shape[1],
        shapley_config)
    np.random.seed(0)
    shapley_values_2 = estimate_shapley_values(
        lambda subset: _set_function_for_aggregated_feature_attribution(subset, X, model),
        X.shape[1],
        shapley_config)

    assert shapley_values_1 == approx(shapley_values_2, abs=0)


def test_estimate_shapley_values_symmetry_approximation_via_early_stopping_with_random_seed(
        preserve_random_generator_state):
    X, coefficients = _generate_data(15)

    def model(x): return np.sum(coefficients * x, axis=1)

    shapley_config = ShapleyConfig(approximation_method=ShapleyApproximationMethods.EARLY_STOPPING)
    assert estimate_shapley_values(
        lambda subset: _set_function_for_aggregated_feature_attribution(subset, X, model),
        X.shape[1],
        shapley_config) != approx(
        estimate_shapley_values(
            lambda subset: _set_function_for_aggregated_feature_attribution(subset, X, model),
            X.shape[1],
            shapley_config), abs=0)

    np.random.seed(0)
    shapley_values_1 = estimate_shapley_values(
        lambda subset: _set_function_for_aggregated_feature_attribution(subset, X, model),
        X.shape[1],
        shapley_config)
    np.random.seed(0)
    shapley_values_2 = estimate_shapley_values(
        lambda subset: _set_function_for_aggregated_feature_attribution(subset, X, model),
        X.shape[1],
        shapley_config)

    assert shapley_values_1 == approx(shapley_values_2, abs=0)


def _generate_data(num_vars):
    return np.random.normal(0, 1, (1000, num_vars)), np.random.choice(20, num_vars) - 10


def _set_function_for_aggregated_feature_attribution(subset, X, model):
    tmp = _permute_features(X, np.arange(0, X.shape[1])[subset == 0], False)
    tmp[:, subset == 1] = X[0, subset == 1]

    return means_difference(model(tmp), X[0])


def _permute_features(feature_samples: np.ndarray,
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


