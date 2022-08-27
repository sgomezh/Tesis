import pytest

from sklearn import linear_model
import dowhy
import dowhy.datasets
from dowhy import CausalModel
import pandas as pd


class TestCausalModel(object):
    @pytest.mark.parametrize(["beta", "num_samples", "num_treatments"],
        [(10, 100, 1),])
    def test_external_estimator(self, beta, num_samples, num_treatments):
        num_common_causes = 5
        data = dowhy.datasets.linear_dataset(
            beta=beta,
            num_common_causes=num_common_causes,
            num_samples=num_samples,
            num_treatments=num_treatments,
            treatment_is_binary=True,
        )

        model = CausalModel(
            data=data["df"],
            treatment=data["treatment_name"],
            outcome=data["outcome_name"],
            graph=data["gml_graph"],
            proceed_when_unidentifiable=True,
            test_significance=None,
        )

        identified_estimand = model.identify_effect(proceed_when_unidentifiable=True)

        estimate = model.estimate_effect(
            identified_estimand,
            method_name="backdoor.tests.causal_estimators.mock_external_estimator.PropensityScoreWeightingEstimator",
            control_value=0,
            treatment_value=1,
            target_units="ate",  # condition used for CATE
            confidence_intervals=True,
            method_params={
                "propensity_score_model": linear_model.LogisticRegression(max_iter=1000)
            },
        )

        assert estimate.estimator.propensity_score_model.max_iter == 1000
        
    @pytest.mark.parametrize(["beta", "num_instruments", "num_samples", "num_treatments"],
                             [(10, 1, 100, 1),])
    def test_graph_input(self, beta, num_instruments, num_samples, num_treatments):
        num_common_causes = 5
        data = dowhy.datasets.linear_dataset(beta=beta,
                                             num_common_causes=num_common_causes,
                                             num_instruments=num_instruments,
                                             num_samples=num_samples,
                                             num_treatments = num_treatments,
                                             treatment_is_binary=True)
        
        model = CausalModel(
            data=data['df'],
            treatment=data["treatment_name"],
            outcome=data["outcome_name"],
            graph=data["gml_graph"],
            proceed_when_unidentifiable=True,
            test_significance=None
        )
        # removing two common causes
        gml_str = 'graph[directed 1 node[ id "{0}" label "{0}"]node[ id "{1}" label "{1}"]node[ id "Unobserved Confounders" label "Unobserved Confounders"]edge[source "{0}" target "{1}"]edge[source "Unobserved Confounders" target "{0}"]edge[source "Unobserved Confounders" target "{1}"]node[ id "X0" label "X0"] edge[ source "X0" target "{0}"] node[ id "X1" label "X1"] edge[ source "X1" target "{0}"] node[ id "X2" label "X2"] edge[ source "X2" target "{0}"] edge[ source "X0" target "{1}"] edge[ source "X1" target "{1}"] edge[ source "X2" target "{1}"] node[ id "Z0" label "Z0"] edge[ source "Z0" target "{0}"]]'.format(data["treatment_name"][0], data["outcome_name"])
        print(gml_str)
        model = CausalModel(
            data=data['df'],
            treatment=data["treatment_name"],
            outcome=data["outcome_name"],
            graph=gml_str,
            proceed_when_unidentifiable=True,
            test_significance=None,
            missing_nodes_as_confounders=True
        )
        common_causes = model.get_common_causes()
        assert all(node_name in common_causes for node_name in ["X1", "X2"])

    @pytest.mark.parametrize(["beta", "num_instruments", "num_samples", "num_treatments"],
                             [(10, 1, 100, 1),])
    def test_graph_input2(self, beta, num_instruments, num_samples, num_treatments):
        num_common_causes = 5
        data = dowhy.datasets.linear_dataset(beta=beta,
                                             num_common_causes=num_common_causes,
                                             num_instruments=num_instruments,
                                             num_samples=num_samples,
                                             num_treatments = num_treatments,
                                             treatment_is_binary=True)

        model = CausalModel(
            data=data['df'],
            treatment=data["treatment_name"],
            outcome=data["outcome_name"],
            graph=data["gml_graph"],
            proceed_when_unidentifiable=True,
            test_significance=None
        )
        # removing two common causes
        gml_str = """graph[
        directed 1 
        node[ id "{0}" 
        label "{0}"
        ]
        node [ 
        id "{1}" 
        label "{1}"
        ]
        node [ 
        id "Unobserved Confounders" 
        label "Unobserved Confounders"
        ]
        edge[
        source "{0}" 
        target "{1}"
        ]
        edge[
        source "Unobserved Confounders" 
        target "{0}"
        ]
        edge[
        source "Unobserved Confounders" 
        target "{1}"
        ]
        node[ 
        id "X0" 
        label "X0"
        ] 
        edge[ 
        source "X0" 
        target "{0}"
        ] 
        node[ 
        id "X1" 
        label "X1"
        ] 
        edge[ 
        source "X1" 
        target "{0}"
        ] 
        node[ 
        id "X2" 
        label "X2"
        ] 
        edge[ 
        source "X2" 
        target "{0}"
        ] 
        edge[ 
        source "X0" 
        target "{1}"
        ] 
        edge[ 
        source "X1" 
        target "{1}"
        ] 
        edge[ 
        source "X2" 
        target "{1}"
        ] 
        node[ 
        id "Z0" 
        label "Z0"
        ] 
        edge[
        source "Z0" 
        target "{0}"
        ]]""".format(data["treatment_name"][0], data["outcome_name"])
        print(gml_str)
        model = CausalModel(
            data=data['df'],
            treatment=data["treatment_name"],
            outcome=data["outcome_name"],
            graph=gml_str,
            proceed_when_unidentifiable=True,
            test_significance=None,
            missing_nodes_as_confounders=True
        )
        common_causes = model.get_common_causes()
        assert all(node_name in common_causes for node_name in ["X1", "X2"])
    
    @pytest.mark.parametrize(["beta", "num_instruments", "num_samples", "num_treatments"],
                             [(10, 1, 100, 1),])
    def test_graph_input3(self, beta, num_instruments, num_samples, num_treatments):
        num_common_causes = 5
        data = dowhy.datasets.linear_dataset(beta=beta,
                                             num_common_causes=num_common_causes,
                                             num_instruments=num_instruments,
                                             num_samples=num_samples,
                                             num_treatments = num_treatments,
                                             treatment_is_binary=True)
        model = CausalModel(
            data=data['df'],
            treatment=data["treatment_name"],
            outcome=data["outcome_name"],
            graph=data["gml_graph"],
            proceed_when_unidentifiable=True,
            test_significance=None
        )
        # removing two common causes 
        gml_str = """dag {
        "Unobserved Confounders" [pos="0.491,-1.056"]
        X0 [pos="-2.109,0.057"]
        X1 [adjusted, pos="-0.453,-1.562"]
        X2 [pos="-2.268,-1.210"]
        Z0 [pos="-1.918,-1.735"]
        v0 [latent, pos="-1.525,-1.293"]
        y [outcome, pos="-1.164,-0.116"]
        "Unobserved Confounders" -> v0
        "Unobserved Confounders" -> y
        X0 -> v0
        X0 -> y
        X1 -> v0
        X1 -> y
        X2 -> v0
        X2 -> y
        Z0 -> v0
        v0 -> y
        }
        """
        print(gml_str)
        model = CausalModel(
            data=data['df'],
            treatment=data["treatment_name"],
            outcome=data["outcome_name"],
            graph=gml_str,
            proceed_when_unidentifiable=True,
            test_significance=None,
            missing_nodes_as_confounders=True
        )
        common_causes = model.get_common_causes()
        assert all(node_name in common_causes for node_name in ["X1", "X2"])
        all_nodes = model._graph.get_all_nodes(include_unobserved=True)
        assert all(node_name in all_nodes for node_name in ["Unobserved Confounders", "X0", "X1", "X2", "Z0", "v0", "y"])
        all_nodes = model._graph.get_all_nodes(include_unobserved=False)
        assert "Unobserved Confounders" not in all_nodes
    
    @pytest.mark.parametrize(["beta", "num_instruments", "num_samples", "num_treatments"],
                             [(10, 1, 100, 1),])
    def test_graph_input4(self, beta, num_instruments, num_samples, num_treatments):
        num_common_causes = 5
        data = dowhy.datasets.linear_dataset(beta=beta,
                                             num_common_causes=num_common_causes,
                                             num_instruments=num_instruments,
                                             num_samples=num_samples,
                                             num_treatments = num_treatments,
                                             treatment_is_binary=True)

        model = CausalModel(
            data=data['df'],
            treatment=data["treatment_name"],
            outcome=data["outcome_name"],
            graph=data["gml_graph"],
            proceed_when_unidentifiable=True,
            test_significance=None
        )
        # removing two common causes 
        gml_str = "tests/sample_dag.txt"
        print(gml_str)
        model = CausalModel(
            data=data['df'],
            treatment=data["treatment_name"],
            outcome=data["outcome_name"],
            graph=gml_str,
            proceed_when_unidentifiable=True,
            test_significance=None,
            missing_nodes_as_confounders=True
        )
        common_causes = model.get_common_causes()
        assert all(node_name in common_causes for node_name in ["X1", "X2"])
        all_nodes = model._graph.get_all_nodes(include_unobserved=True)
        assert all(node_name in all_nodes for node_name in ["Unobserved Confounders", "X0", "X1", "X2", "Z0", "v0", "y"])
        all_nodes = model._graph.get_all_nodes(include_unobserved=False)
        assert "Unobserved Confounders" not in all_nodes

    @pytest.mark.parametrize(["num_variables", "num_samples"],
                             [(10,5000),])
    def test_graph_refutation(self, num_variables,num_samples):
        data = dowhy.datasets.dataset_from_random_graph(num_vars = num_variables, num_samples= num_samples)
        df = data["df"]
        model = CausalModel(
            data=df,
            treatment=data["treatment_name"],
            outcome=data["outcome_name"],
            graph=data["gml_graph"],
        )
        graph_refutation_object = model.refute_graph(k = 1, independence_test = 
        {'test_for_continuous': 'partial_correlation', 
        'test_for_discrete' : 'conditional_mutual_information'})
        assert graph_refutation_object.refutation_result == True

    @pytest.mark.parametrize(["num_variables", "num_samples"],
                             [(10,5000),])
    def test_graph_refutation2(self, num_variables,num_samples):
        data = dowhy.datasets.dataset_from_random_graph(num_vars = num_variables, num_samples= num_samples)
        df = data["df"]
        gml_str = """
        graph [
        directed 1
        node [
            id 0
            label "a"
        ]
        node [
            id 1
            label "b"
        ]
        node [
            id 2
            label "c"
        ]
        node [
            id 3
            label "d"
        ]
        node [
            id 4
            label "e"
        ]
        node [
            id 5
            label "f"
        ]
        node [
            id 6
            label "g"
        ]
        node [
            id 7
            label "h"
        ]
        node [
            id 8
            label "i"
        ]
        node [
            id 9
            label "j"
        ]
        edge [
            source 0
            target 1
        ]
        edge [
            source 0
            target 3
        ]
        edge [
            source 3
            target 2
        ]
        edge [
            source 7
            target 4
        ]
        edge [
            source 6
            target 5
        ]
        edge [
            source 7
            target 8
        ]
        edge [
            source 9
            target 2
        ]
        edge [
            source 9
            target 8
        ]
        ]
        """
        model = CausalModel(
            data=df,
            treatment=data["treatment_name"],
            outcome=data["outcome_name"],
            graph=gml_str,
        )
        graph_refutation_object = model.refute_graph(k = 2, independence_test = 
        {'test_for_continuous': 'partial_correlation', 
        'test_for_discrete' : 'conditional_mutual_information'})
        assert graph_refutation_object.refutation_result == False

if __name__ == "__main__":
    pytest.main([__file__])
