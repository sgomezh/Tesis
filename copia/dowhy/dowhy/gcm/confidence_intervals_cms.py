"""This module provides functionality to estimate confidence intervals via bootstrapping the fitting and sampling.

Functions in this module should be considered experimental, meaning there might be breaking API changes in the future.
"""

from functools import partial
from typing import Union, Callable, Any, Dict

import numpy as np
import pandas as pd

from dowhy.gcm.cms import ProbabilisticCausalModel, InvertibleStructuralCausalModel, StructuralCausalModel
from dowhy.gcm.fitting_sampling import fit

# A convenience function when computing confidence intervals specifically for non-deterministic causal queries. This
# function evaluates the provided causal query multiple times to build a confidence interval based on the returned
# results.
# Note that this function does not re-fit the causal model(s) and only executes the provided query as it is. In order
# to re-refit the graphical causal model on random subsets of the data before executing the query, consider using the
# bootstrap_training_and_sampling function.
#
# **Example usage:**
#
#     >>> gcm.fit(causal_model, data)
#     >>> strength_medians, strength_intervals = gcm.confidence_intervals(
#     >>>     gcm.bootstrap_sampling(gcm.arrow_strength, causal_model, target_node='Y'))
#
# In this example, gcm.confidence_intervals is expecting a callable with non-deterministic outputs for building the
# confidence intervals. Since each causal query potentially expects a different set of parameters, we use 'partial'
# here to configure the function call. In this case,
# gcm.bootstrap_sampling(gcm.arrow_strength, causal_model, target_node='Y') would be equivalent to
# lambda : gcm.arrow_strength(causal_model, target_node='Y').
#
# In order to incorporate uncertainties coming from fitting the causal model(s), we can use
# gcm.bootstrap_training_and_sampling instead:
# >>>  strength_medians, strength_intervals = gcm.confidence_intervals(
# >>>        gcm.bootstrap_training_and_sampling(gcm.arrow_strength,
# >>>                                            causal_model,
# >>>                                            bootstrap_training_data=data,
# >>>                                            target_node='Y'))
# This would refit the provided causal_model on a subset of the data first before executing gcm.arrow_strength in each
# run.
bootstrap_sampling = partial


def bootstrap_training_and_sampling(f: Callable[[Union[ProbabilisticCausalModel,
                                                       StructuralCausalModel,
                                                       InvertibleStructuralCausalModel], Any],
                                                Dict[Any, Union[np.ndarray, float]]],
                                    causal_model: Union[ProbabilisticCausalModel,
                                                        StructuralCausalModel,
                                                        InvertibleStructuralCausalModel],
                                    bootstrap_training_data: pd.DataFrame,
                                    bootstrap_data_subset_size_fraction: float = 0.75,
                                    *args, **kwargs):
    """A convenience function when computing confidence intervals specifically for causal queries. This function
    specifically bootstraps training *and* sampling.

    **Example usage:**

        >>> scores_median, scores_intervals = gcm.confidence_intervals(
        >>>     gcm.bootstrap_training_and_sampling(gcm.arrow_strength,
        >>>                                         causal_model,
        >>>                                         bootstrap_training_data=data,
        >>>                                         target_node='Y'))

    :param f: The causal query to perform. A causal query is a function taking a graphical causal model as first
              parameter and an arbitrary number of remaining parameters. It must return a dictionary with
              attribution-like data.
    :param causal_model: A graphical causal model to perform the causal query on. It need not be fitted.
    :param bootstrap_training_data: The training data to use when fitting. A random subset from this data set is used
                                    in every iteration when calling fit.
    :param bootstrap_data_subset_size_fraction: The fraction defines the fractional size of the subset compared to
                                                the total training data.
    :param args: Args passed through verbatim to the causal queries.
    :param kwargs: Keyword args passed through verbatim to the causal queries.
    :return: A tuple containing (1) the median of causal query results and (2) the confidence intervals.
    """

    def snapshot():
        causal_model_copy = causal_model.clone()
        sampled_data = bootstrap_training_data.iloc[
            np.random.choice(bootstrap_training_data.shape[0],
                             int(bootstrap_training_data.shape[0] * bootstrap_data_subset_size_fraction),
                             replace=False)
        ]
        fit(causal_model_copy, sampled_data)
        return f(causal_model_copy, *args, **kwargs)

    return snapshot
