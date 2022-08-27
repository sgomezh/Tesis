"""This module defines multiple implementations of the abstract class :class:`~dowhy.gcm.graph.FunctionalCausalModel`
(FCM)

Classes in this module should be considered experimental, meaning there might be breaking API changes in the future.
"""

import copy
from abc import abstractmethod, ABC
from typing import Optional, List

import numpy as np

from dowhy.gcm.graph import StochasticModel, FunctionalCausalModel, InvertibleFunctionalCausalModel
from dowhy.gcm.util.general import shape_into_2d, is_categorical


class PredictionModel:
    """ Represents general prediction model implementations. Each prediction model should provide a fit and a predict
        method. """

    @abstractmethod
    def fit(self, X: np.ndarray, Y: np.ndarray) -> None:
        raise NotImplementedError

    @abstractmethod
    def predict(self, X: np.ndarray) -> np.ndarray:
        raise NotImplementedError

    @abstractmethod
    def clone(self):
        """
        Clones the prediction model using the same hyper parameters but not fitted.

        :return: An unfitted clone of the prediction model.
        """
        raise NotImplementedError


class ClassificationModel(PredictionModel):

    @abstractmethod
    def predict_probabilities(self, X: np.array) -> np.ndarray:
        raise NotImplementedError

    @abstractmethod
    def classes(self) -> List[str]:
        raise NotImplementedError


class InvertibleFunction:

    @abstractmethod
    def evaluate(self, X: np.ndarray) -> np.ndarray:
        """ Applies the function on the input. """
        raise NotImplementedError

    @abstractmethod
    def evaluate_inverse(self, X: np.ndarray) -> np.ndarray:
        """ Returns the outcome of applying the inverse of the function on the inputs. """
        raise NotImplementedError


class PostNonlinearModel(InvertibleFunctionalCausalModel):
    """
        Represents an post nonlinear FCM, i.e. models of the form:
            Y = g(f(X) + N),
        where X are parent nodes of the target node Y, f an arbitrary prediction model expecting inputs from the
        parents X, N a noise variable and g an invertible function.
    """

    def __init__(self,
                 prediction_model: PredictionModel,
                 noise_model: StochasticModel,
                 invertible_function: InvertibleFunction) -> None:
        """
        :param prediction_model: The prediction model f.
        :param invertible_function: The invertible function g.
        :param noise_model: The StochasticModel to describe the distribution of the noise N.
        """
        self._prediction_model = prediction_model
        self._noise_model = noise_model
        self._invertible_function = invertible_function

    def fit(self, X: np.ndarray, Y: np.ndarray) -> None:
        """Fits the post non-linear model of the form Y = g(f(X) + N). Here, this consists of three steps given
        samples from (X, Y):

            1. Transform Y via the inverse of g: g^-1(Y) = f(X) + N
            2. Fit the model for f on (X, g^-1(Y))
            3. Reconstruct N based on the residual N = g^-1(Y) - f(X)

        Note that the noise here can be inferred uniquely if the model assumption holds.

        :param X: Samples from the input X.
        :param Y: Samples from the target Y.
        :return: None
        """
        X, Y = shape_into_2d(X, Y)

        self._prediction_model.fit(X=X, Y=self._invertible_function.evaluate_inverse(Y))
        self._noise_model.fit(X=self.estimate_noise(Y, X))

    def estimate_noise(self,
                       target_samples: np.ndarray,
                       parent_samples: np.ndarray) -> np.ndarray:
        """Reconstruct the noise given samples from (X, Y). This is done by:

            1. Transform Y via the inverse of g: g^-1(Y) = f(X) + N
            2. Return the residual g^-1(Y) - f(X)

        :param target_samples: Samples from the input X.
        :param parent_samples: Samples from the target Y.
        :return: The reconstructed noise based on the given samples.
        """
        target_samples, parent_samples = shape_into_2d(target_samples, parent_samples)

        return self._invertible_function.evaluate_inverse(target_samples) - self._prediction_model.predict(
            parent_samples)

    def draw_noise_samples(self, num_samples: int) -> np.ndarray:
        """Draws samples from the noise distribution N.

        :param num_samples: Number of noise samples.
        :return: A numpy array containing num_samples samples from the noise.
        """
        return self._noise_model.draw_samples(num_samples)

    def evaluate(self, parent_samples: np.ndarray, noise_samples: np.ndarray) -> np.ndarray:
        """Evaluates the post non-linear model given samples (X, N). This is done by:

            1. Evaluate f(X)
            2. Evaluate f(X) + N
            3. Return g(f(X) + N)

        :param parent_samples: Samples from the inputs X.
        :param noise_samples: Samples from the noise N.
        :return: The Y values based on the given samples.
        """
        parent_samples, noise_samples = shape_into_2d(parent_samples, noise_samples)
        predictions = shape_into_2d(self._prediction_model.predict(parent_samples))

        return self._invertible_function.evaluate(predictions + noise_samples)

    def __str__(self) -> str:
        return '%s with %s and an %s' % (self.__class__.__name__,
                                         self._prediction_model.__class__.__name__,
                                         self._invertible_function.__class__.__name__)

    def clone(self):
        return PostNonlinearModel(prediction_model=self._prediction_model.clone(),
                                  noise_model=self._noise_model.clone(),
                                  invertible_function=copy.deepcopy(self._invertible_function))

    @property
    def prediction_model(self) -> PredictionModel:
        return self._prediction_model

    @property
    def noise_model(self) -> StochasticModel:
        return self._noise_model

    @property
    def invertible_function(self) -> InvertibleFunction:
        return self._invertible_function


class AdditiveNoiseModel(PostNonlinearModel):
    """Represents the continuous functional causal model of the form
        Y = f(X) + N,
    where X is the input (typically, direct causal parents of Y) and the noise N is assumed to be independent of X. This
    is a special instance of a :py:class:`PostNonlinearModel <dowhy.gcm.PostNonlinearModel>` where the function g is the
    identity function.

    Given joint samples from (X, Y), this model can be fitted by first training a model f (e.g. using least squares
    regression) and then reconstruct N by N = Y - f(X), i.e. using the residual.
    """
    def __init__(self,
                 prediction_model: PredictionModel,
                 noise_model: Optional[StochasticModel] = None) -> None:
        if noise_model is None:
            from dowhy.gcm.stochastic_models import EmpiricalDistribution
            noise_model = EmpiricalDistribution()

        from dowhy.gcm.ml.regression import InvertibleIdentityFunction
        super(AdditiveNoiseModel, self).__init__(prediction_model=prediction_model,
                                                 noise_model=noise_model,
                                                 invertible_function=InvertibleIdentityFunction())

    def clone(self):
        return AdditiveNoiseModel(prediction_model=self.prediction_model.clone(),
                                  noise_model=self.noise_model.clone())


class ProbabilityEstimatorModel(ABC):
    @abstractmethod
    def estimate_probabilities(self, parent_samples: np.ndarray) -> np.ndarray:
        raise NotImplementedError


class ClassifierFCM(FunctionalCausalModel, ProbabilityEstimatorModel):
    """Represents the categorical functional causal model of the form
        Y = f(X, N),
    where X is the input (typically, direct causal parents of Y) and the noise N here is uniform on [0, 1]. The model
    is mostly based on a standard classification model that outputs probabilities. In order to generate a new random
    sample given an input x, the return value y is uniformly sampled based on the class probabilities p(y | x). Here,
    the noise is used to make this sampling process deterministic by using the cumulative distribution functions defined
    by the given inputs.
    """
    def __init__(self, classifier_model: Optional[ClassificationModel] = None) -> None:
        self._classifier_model = classifier_model

        if classifier_model is None:
            from dowhy.gcm.ml.classification import create_hist_gradient_boost_classifier
            self._classifier_model = create_hist_gradient_boost_classifier()

    def draw_noise_samples(self, num_samples: int) -> np.ndarray:
        """Returns uniformly sampled values on [0, 1].

        :param num_samples: Number of noise samples.
        :return: Noise samples on [0, 1].
        """
        return shape_into_2d(np.random.uniform(0, 1, num_samples))

    def evaluate(self, parent_samples: np.ndarray, noise_samples: np.ndarray) -> np.ndarray:
        """Evaluates the model Y = f(X, N), where X are the parent_samples and N the noise_samples. Here, the
        cumulative distribution functions are defined by the parent_samples. For instance, lets say we have 2
        classes, n = 0.7 and an input x with p(y = 0| x) = 0.6 and p(y = 1| x) = 0.4, then we get y = 1 as a return
        value. This is because p(y = 0| x) < n <= 1.0, i.e. n falls into the bucket that is spanned by p(y = 1| x).

        :param parent_samples: Samples from the inputs X.
        :param noise_samples: Samples from the noise on [0, 1].
        :return: Class labels Y based on the inputs and noise.
        """
        noise_samples = shape_into_2d(noise_samples)
        probabilities = self.estimate_probabilities(parent_samples)

        probabilities = np.cumsum(probabilities, axis=1) - noise_samples
        probabilities[probabilities < 0] = 1

        return shape_into_2d(np.array(self.get_class_names(np.argmin(probabilities, axis=1))))

    def estimate_probabilities(self, parent_samples: np.ndarray) -> np.ndarray:
        """Returns the class probabilities for the given parent_samples.

        :param parent_samples: Samples from inputs X.
        :return: A nxd numpy matrix with class probabilities for each sample, where n is the number of samples and d
                 the number of classes. Here, array entry A[i][j] corresponds to the i-th sample indicating the
                 probability of the j-th class.
        """
        return self._classifier_model.predict_probabilities(parent_samples)

    def fit(self, X: np.ndarray, Y: np.ndarray) -> None:
        """Fits the underlying classification model.

        :param X: Input samples.
        :param Y: Target labels.
        :return: None
        """
        X, Y = shape_into_2d(X, Y)

        if not is_categorical(Y):
            raise ValueError("The target data needs to be categorical in the form of strings!")

        self._classifier_model.fit(X=X, Y=Y)

    def clone(self):
        return ClassifierFCM(classifier_model=self._classifier_model.clone())

    def get_class_names(self, class_indices: np.ndarray) -> List[str]:
        return [self._classifier_model.classes()[index] for index in class_indices]

    @property
    def classifier_model(self) -> ClassificationModel:
        return self._classifier_model
