Code repository & Versions
==========================

DoWhy is hosted on GitHub.

You can browse the code in a html-friendly format `here
<https://github.com/Microsoft/dowhy>`_.

v0.7.1: Added Graph refuter. Support for dagitty graphs and external estimators
--------------------------------------------------------------------------------------

* Graph refuter with conditional independence tests to check whether data conforms to the assumed causal graph

* Better docs for estimators by adding the method-specific parameters directly in its own init method

* Support use of custom external estimators 

* Consistent structure for init_params for dowhy and econml estimators

* Add support for Dagitty graphs

* Bug fixes for GLM model, causal model with no confounders, and hotel case-study notebook

Thank you @EgorKraevTransferwise, @ae-foster, @anusha0409 for your contributions! 

v0.7: Better Refuters for unobserved confounders and placebo treatment
----------------------------------------------------------------------
* **[Major]** Faster backdoor identification with support for minimal adjustment, maximal adjustment
  or exhaustive search. More test coverage for identification.

* **[Major]** Added new functionality of causal discovery [Experimental].
  DoWhy now supports discovery algorithms from external libraries like CDT.
  `[Example notebook] <https://github.com/microsoft/dowhy/blob/master/docs/source/example_notebooks/dowhy_causal_discovery_example.ipynb>`_

* **[Major]** Implemented ID algorithm for causal identification. [Experimental] 

* Added friendly text-based interpretation for DoWhy's effect estimate. 

* Added a new estimation method, distance matching that relies on a distance
  metrics between inputs.
  
* Heuristics to infer default parameters for refuters. 

* Inferring default strata automatically for propensity score stratification.
 
* Added support for custom propensity models in propensity-based estimation
  methods. 

* Bug fixes for confidence intervals for linear regression. Better version of
  bootstrap method.

* Allow effect estimation without need to refit the model for econml estimators

Big thanks to @AndrewC19, @ha2trinh, @siddhanthaldar, and @vojavocni 

v0.6: Better Refuters for unobserved confounders and placebo treatment
----------------------------------------------------------------------

* **[Major]** Placebo refuter also works for IV methods

* **[Major]** Moved matplotlib to an optional dependency. Can be installed using `pip install dowhy[plotting]`

* **[Major]** A new method for generating unobserved confounder for refutation

* Update to align with EconML's new API

* All refuters now support control and treatment values for continuous treatments

* Better logging configuration

* Dummyoutcomerefuter supports unobserved confounder

A big thanks to @arshiaarya, @n8sty, @moprescu and @vojavocni

v0.5-beta: Enhanced documentation and support for causal mediation
-------------------------------------------------------------------

**Installation**

* DoWhy can be installed on Conda now! 

**Code**

* Support for identification by mediation formula

* Support for the front-door criterion

* Linear estimation methods for mediation

* Generalized backdoor criterion implementation using paths and d-separation

* Added GLM estimators, including logistic regression

* New API for interpreting causal models, estimates and refuters. First
  interpreter by @ErikHambardzumyan visualizes how the distribution of confounder changes

* Friendlier error messages for propensity score stratification estimator when there is not enough data in a bin

* Enhancements to the dummy outcome refuter with machine learned components--now can simulate non-zero effects too. Ready for alpha testing


**Docs**

* New case studies using DoWhy on `hotel booking cancellations <https://github.com/microsoft/dowhy/blob/master/docs/source/example_notebooks/DoWhy-The%20Causal%20Story%20Behind%20Hotel%20Booking%20Cancellations.ipynb>`_ and `membership rewards programs <https://github.com/microsoft/dowhy/blob/master/docs/source/example_notebooks/dowhy_example_effect_of_memberrewards_program.ipynb>`_

* New `notebook <https://github.com/microsoft/dowhy/blob/master/docs/source/example_notebooks/dowhy_multiple_treatments.ipynb>`_ on using DoWhy+EconML for estimating effect of multiple treatments

* A `tutorial  <https://github.com/microsoft/dowhy/blob/master/docs/source/example_notebooks/tutorial-causalinference-machinelearning-using-dowhy-econml.ipynb>`_ on causal inference using DoWhy and EconML

* Better organization of docs and notebooks on the `documentation website <https://py-why.github.io/dowhy/>`_.

**Community**

* Created a `contributors page <https://github.com/microsoft/dowhy/blob/master/CONTRIBUTING.md>`_ with guidelines for contributing

* Added allcontributors bot so that new contributors can added just after their pull requests are merged

A big thanks to @Tanmay-Kulkarni101, @ErikHambardzumyan, @Sid-darthvader for their contributions. 

v0.4-beta: Powerful refutations and better support for heterogeneous treatment effects
--------------------------------------------------------------------------------------

* DummyOutcomeRefuter now includes machine learning functions to increase power of the refutation.
	* In addition to generating a random dummy outcome, now you can generate a dummyOutcome that is an arbitrary function of confounders but always independent of treatment, and then test whether the estimated treatment effect is zero. This is inspired by ideas from the T-learner.
	* We also provide default machine learning-based methods to estimate such a dummyOutcome based on confounders. Of course, you can specify any custom ML method.

* Added a new BootstrapRefuter that simulates the issue of measurement error with confounders. Rather than a simple bootstrap, you can generate bootstrap samples with noise on the values of the confounders and check how sensitive the estimate is.
	* The refuter supports custom selection of the confounders to add noise to.

* All refuters now provide confidence intervals and a significance value.

* Better support for heterogeneous effect libraries like EconML and CausalML
	* All CausalML methods can be called directly from DoWhy, in addition to all methods from EconML.
	* [Change to naming scheme for estimators] To achieve a consistent naming scheme for estimators, we suggest to prepend internal dowhy estimators with the string "dowhy". For example, "backdoor.dowhy.propensity_score_matching". Not a breaking change, so you can keep using the old naming scheme too.
	* EconML-specific: Since EconML assumes that effect modifiers are a subset of confounders, a warning is issued if a user specifies effect modifiers outside of confounders and tries to use EconML methods.

* CI and Standard errors: Added bootstrap-based confidence intervals and standard errors for all methods. For linear regression estimator, also implemented the corresponding parametric forms.

* Convenience functions for getting confidence intervals, standard errors and conditional treatment effects (CATE), that can be called after fitting the estimator if needed

* Better coverage for tests. Also, tests are now seeded with a random seed, so more dependable tests.

Thanks to @Tanmay-Kulkarni101 and @Arshiaarya for their contributions!

v0.2-alpha: CATE estimation and integration with EconML
-------------------------------------------------------


This release includes many major updates:

* (BREAKING CHANGE) The CausalModel import is now simpler: "from dowhy import CausalModel"
*  Multivariate treatments are now supported. 
*  Conditional Average Treatment Effects (CATE) can be estimated for any subset of the data. Includes integration with EconML--any method from EconML can be called using DoWhy through the estimate_effect method (see example notebook). 
*  Other than CATE, specific target estimands like ATT and ATC are also supported for many of the estimation methods.   
* For reproducibility, you can specify a random seed for all refutation methods. 
* Multiple bug fixes and updates to the documentation.

 
Includes contributions from @j-chou, @ktmud, @jrfiedler, @shounak112358, @Lnk2past. Thank you all!

v0.1.1-alpha: First release
---------------------------
This is the first release of the library.
