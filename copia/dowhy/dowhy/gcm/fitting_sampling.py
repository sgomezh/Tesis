"""This module provides functionality for fitting probabilistic causal models and drawing samples from them.

Functions in this module should be considered experimental, meaning there might be breaking API changes in the future.
"""

from typing import Any

import networkx as nx
import pandas as pd
from tqdm import tqdm

from dowhy.gcm import config
from dowhy.gcm.cms import ProbabilisticCausalModel
from dowhy.gcm.graph import get_ordered_predecessors, is_root_node, PARENTS_DURING_FIT, \
    validate_causal_model_assignment, validate_causal_dag
from dowhy.gcm.util.general import column_stack_selected_numpy_arrays, convert_to_data_frame


def fit(causal_model: ProbabilisticCausalModel, data: pd.DataFrame):
    """Learns generative causal models of nodes in the causal graph from data.

    :param causal_model: The causal model containing the mechanisms that will be fitted.
    :param data: Observations of nodes in the causal model.
    """
    progress_bar = tqdm(causal_model.graph.nodes, desc='Fitting causal models', position=0, leave=True,
                        disable=not config.show_progress_bars)
    for node in progress_bar:
        if node not in data:
            raise RuntimeError('Could not find data for node %s in the given training data! There should be a column '
                               'containing samples for node %s.' % (node, node))

        progress_bar.set_description('Fitting causal mechanism of node %s' % node)

        fit_causal_model_of_target(causal_model, node, data)


def fit_causal_model_of_target(causal_model: ProbabilisticCausalModel,
                               target_node: Any,
                               training_data: pd.DataFrame) -> None:
    """Fits only the causal mechanism of the given target node based on the training data.

    :param causal_model: The causal model containing the target node.
    :param target_node: Target node for which the mechanism is fitted.
    :param training_data: Training data for fitting the causal mechanism.
    :return: None
    """
    validate_causal_model_assignment(causal_model.graph, target_node)

    if is_root_node(causal_model.graph, target_node):
        causal_model.causal_mechanism(target_node).fit(X=training_data[target_node].to_numpy())
    else:
        causal_model.causal_mechanism(target_node).fit(
            X=training_data[get_ordered_predecessors(causal_model.graph, target_node)].to_numpy(),
            Y=training_data[target_node].to_numpy())

    # To be able to validate that the graph structure did not change between fitting and causal query, we store the
    # parents of a node during fit. That way, before sampling, we can verify the parents are still the same. While
    # this would automatically fail when the number of parents is different, there are other more subtle cases,
    # where the number is still the same, but it's different parents, and therefore different data. That would yield
    # wrong results, but would not fail.
    causal_model.graph.nodes[target_node][PARENTS_DURING_FIT] = \
        get_ordered_predecessors(causal_model.graph, target_node)


def draw_samples(causal_model: ProbabilisticCausalModel, num_samples: int) -> pd.DataFrame:
    """Draws new joint samples from the given graphical causal model. This is done by first generating random samples
    from root nodes and then propagating causal downstream effects through the graph.

    :param causal_model: New samples are generated based on the given causal model.
    :param num_samples: Number of samples to draw.
    :return: A pandas data frame where columns correspond to the nodes in the graph and rows to the drawn joint samples.
    """
    validate_causal_dag(causal_model.graph)

    drawn_samples = {}

    for node in nx.topological_sort(causal_model.graph):
        if is_root_node(causal_model.graph, node):
            drawn_samples[node] = causal_model.causal_mechanism(node).draw_samples(num_samples)
        else:
            drawn_samples[node] = causal_model.causal_mechanism(node).draw_samples(
                column_stack_selected_numpy_arrays(drawn_samples, get_ordered_predecessors(causal_model.graph, node)))

    return convert_to_data_frame(drawn_samples)
