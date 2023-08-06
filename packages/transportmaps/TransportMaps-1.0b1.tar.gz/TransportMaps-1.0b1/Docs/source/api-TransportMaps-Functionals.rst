TransportMaps.Functionals
=============================================

**Classes**


.. inheritance-diagram:: TransportMaps.Functionals.Function TransportMaps.Functionals.ParametricFunctionApproximation TransportMaps.Functionals.TensorizedFunctionApproximation TransportMaps.Functionals.LinearSpanApproximation TransportMaps.Functionals.IntegratedSquaredParametricFunctionApproximation TransportMaps.Functionals.MonotonicFunctionApproximation TransportMaps.Functionals.MonotonicLinearSpanApproximation TransportMaps.Functionals.MonotonicIntegratedExponentialApproximation TransportMaps.Functionals.MonotonicIntegratedSquaredApproximation TransportMaps.Functionals.MonotonicFrozenFunction TransportMaps.Functionals.FrozenLinear TransportMaps.Functionals.FrozenExponential TransportMaps.Functionals.FrozenGaussianToUniform TransportMaps.Functionals.LogLikelihood
   :parts: 1


====================================================================================================================================================================  =====================================================================================================================================================================
`Function <api-TransportMaps-Functionals.html\#TransportMaps.Functionals.Function>`_                                                                                  Abstract class for parametric approximation :math:`f_{\bf a}:\mathbb{R}^d\rightarrow\mathbb{R}` of :math:`f:\mathbb{R}^d\rightarrow\mathbb{R}`.
`ParametricFunctionApproximation <api-TransportMaps-Functionals.html\#TransportMaps.Functionals.ParametricFunctionApproximation>`_                                    Abstract class for parametric approximation :math:`f_{\bf a}:\mathbb{R}^d\rightarrow\mathbb{R}` of :math:`f:\mathbb{R}^d\rightarrow\mathbb{R}`.
`TensorizedFunctionApproximation <api-TransportMaps-Functionals.html\#TransportMaps.Functionals.TensorizedFunctionApproximation>`_                                    [Abstract] Class for approximations using tensorization of unidimensional basis
`LinearSpanApproximation <api-TransportMaps-Functionals.html\#TransportMaps.Functionals.LinearSpanApproximation>`_                                                    Parametric function :math:`f_{\bf a} = \sum_{{\bf i} \in \mathcal{I}} {\bf a}_{\bf i} \Phi_{\bf i}`
`IntegratedSquaredParametricFunctionApproximation <api-TransportMaps-Functionals.html\#TransportMaps.Functionals.IntegratedSquaredParametricFunctionApproximation>`_  Parameteric function :math:`f_{\bf a}({\bf x}) = \int_0^{x_d} h_{\bf a}^2(x_1,\ldots,x_{d-1},t) dt`
`MonotonicFunctionApproximation <api-TransportMaps-Functionals.html\#TransportMaps.Functionals.MonotonicFunctionApproximation>`_                                      Abstract class for the approximation :math:`f \approx f_{\bf a} = \sum_{{\bf i} \in \mathcal{I}} {\bf a}_{\bf i} \Phi_{\bf i}` assumed to be monotonic in :math:`x_d`
`MonotonicLinearSpanApproximation <api-TransportMaps-Functionals.html\#TransportMaps.Functionals.MonotonicLinearSpanApproximation>`_                                  Approximation of the type :math:`f \approx f_{\bf a} = \sum_{{\bf i} \in \mathcal{I}} {\bf a}_{\bf i} \Phi_{\bf i}`, monotonic in :math:`x_d`
`MonotonicIntegratedExponentialApproximation <api-TransportMaps-Functionals.html\#TransportMaps.Functionals.MonotonicIntegratedExponentialApproximation>`_            Integrated Exponential approximation.
`MonotonicIntegratedSquaredApproximation <api-TransportMaps-Functionals.html\#TransportMaps.Functionals.MonotonicIntegratedSquaredApproximation>`_                    Integrated Squared approximation.
`MonotonicFrozenFunction <api-TransportMaps-Functionals.html\#TransportMaps.Functionals.MonotonicFrozenFunction>`_                                                    [Abstract] Frozen function. No optimization over the coefficients allowed.
`FrozenLinear <api-TransportMaps-Functionals.html\#TransportMaps.Functionals.FrozenLinear>`_                                                                          Frozen Linear map :math:`{\bf x} \rightarrow a_1 + a_2 {\bf x}_d`
`FrozenExponential <api-TransportMaps-Functionals.html\#TransportMaps.Functionals.FrozenExponential>`_                                                                Frozen Exponential map :math:`f_{\bf a}:{\bf x} \mapsto \exp( {\bf x}_d )`
`FrozenGaussianToUniform <api-TransportMaps-Functionals.html\#TransportMaps.Functionals.FrozenGaussianToUniform>`_                                                    Frozen Gaussian To Uniform map.
`LogLikelihood <api-TransportMaps-Functionals.html\#TransportMaps.Functionals.LogLikelihood>`_                                                                        Abstract class for log-likelihood :math:`\log \pi({\bf y} \vert {\bf x})`
====================================================================================================================================================================  =====================================================================================================================================================================



**Documentation**

.. automodule:: TransportMaps.Functionals
   :members:

