TransportMaps.Maps
=============================================

**Sub-modules**

.. toctree::
   :maxdepth: 1

   api-TransportMaps-Maps-Decomposable


**Classes**


.. inheritance-diagram:: TransportMaps.Maps.TransportMap TransportMaps.Maps.InverseTransportMap TransportMaps.Maps.CompositeTransportMap TransportMaps.Maps.ListCompositeTransportMap TransportMaps.Maps.ListStackedTransportMap TransportMaps.Maps.IdentityTransportMap TransportMaps.Maps.PermutationTransportMap TransportMaps.Maps.LinearTransportMap TransportMaps.Maps.TriangularTransportMap TransportMaps.Maps.MonotonicTriangularTransportMap TransportMaps.Maps.TriangularListStackedTransportMap TransportMaps.Maps.FrozenLinearDiagonalTransportMap TransportMaps.Maps.FrozenExponentialDiagonalTransportMap TransportMaps.Maps.FrozenGaussianToUniformDiagonalTransportMap TransportMaps.Maps.FrozenBananaTransportMap TransportMaps.Maps.IntegratedExponentialTriangularTransportMap TransportMaps.Maps.CommonBasisIntegratedExponentialTriangularTransportMap TransportMaps.Maps.IntegratedSquaredTriangularTransportMap TransportMaps.Maps.LinearSpanTriangularTransportMap TransportMaps.Maps.CommonBasisLinearSpanTriangularTransportMap TransportMaps.Maps.MonotonicLinearSpanTriangularTransportMap TransportMaps.Maps.MonotonicCommonBasisLinearSpanTriangularTransportMap
   :parts: 1


==================================================================================================================================================================  ========================================================================================================================================================================
`TransportMap <api-TransportMaps-Maps.html\#TransportMaps.Maps.TransportMap>`_                                                                                      Transport map :math:`T({\bf x},{\bf a})`.
`InverseTransportMap <api-TransportMaps-Maps.html\#TransportMaps.Maps.InverseTransportMap>`_                                                                        Given the transport map :math:`T`, define :math:`S=T^{-1}`.
`CompositeTransportMap <api-TransportMaps-Maps.html\#TransportMaps.Maps.CompositeTransportMap>`_                                                                    Given transport maps :math:`T_1,T_2`, define transport map :math:`T=T_1 \circ T_2`.
`ListCompositeTransportMap <api-TransportMaps-Maps.html\#TransportMaps.Maps.ListCompositeTransportMap>`_                                                            Construct the composite map :math:`T_1 \circ T_2 \circ \cdots \circ T_n`
`ListStackedTransportMap <api-TransportMaps-Maps.html\#TransportMaps.Maps.ListStackedTransportMap>`_                                                                Defines the transport map :math:`T` obtained by stacking :math:`T_1, T_2, \ldots`.
`IdentityTransportMap <api-TransportMaps-Maps.html\#TransportMaps.Maps.IdentityTransportMap>`_                                                                      Map :math:`T({\bf x})={\bf x}`.
`PermutationTransportMap <api-TransportMaps-Maps.html\#TransportMaps.Maps.PermutationTransportMap>`_                                                                Map :math:`T({\bf x}) = [x_{p(0)}, \ldots, x_{p(d)}]^T`
`LinearTransportMap <api-TransportMaps-Maps.html\#TransportMaps.Maps.LinearTransportMap>`_                                                                          Linear map :math:`T({\bf x})={\bf c} + {\bf L}{\bf x}`
`TriangularTransportMap <api-TransportMaps-Maps.html\#TransportMaps.Maps.TriangularTransportMap>`_                                                                  Generalized triangular transport map :math:`T({\bf x},{\bf a})`.
`MonotonicTriangularTransportMap <api-TransportMaps-Maps.html\#TransportMaps.Maps.MonotonicTriangularTransportMap>`_                                                [Abstract] Triangular transport map which is monotone by construction.
`TriangularListStackedTransportMap <api-TransportMaps-Maps.html\#TransportMaps.Maps.TriangularListStackedTransportMap>`_                                            Triangular transport map obtained by stacking :math:`T_1, T_2, \ldots`.
`FrozenLinearDiagonalTransportMap <api-TransportMaps-Maps.html\#TransportMaps.Maps.FrozenLinearDiagonalTransportMap>`_                                              Linear diagonal transport map :math:`(x_1,\ldots,x_d) \rightarrow (a_1+b_1 x_1, \ldots, a_d + b_d x_d)`
`FrozenExponentialDiagonalTransportMap <api-TransportMaps-Maps.html\#TransportMaps.Maps.FrozenExponentialDiagonalTransportMap>`_                                    Exponential diagonal transport map :math:`(x_1,\ldots,x_d) \rightarrow (\exp(x_1), \ldots, \exp(x_d))`
`FrozenGaussianToUniformDiagonalTransportMap <api-TransportMaps-Maps.html\#TransportMaps.Maps.FrozenGaussianToUniformDiagonalTransportMap>`_                        Gaussian to Uniform diagonal transport map :math:`(x_1,\ldots,x_d) \rightarrow (\frac{1}{2}[1+{\rm erf}(x_1/\sqrt{2})], \ldots, \frac{1}{2}[1+{\rm erf}(x_d/\sqrt{2})])`
`FrozenBananaTransportMap <api-TransportMaps-Maps.html\#TransportMaps.Maps.FrozenBananaTransportMap>`_
`IntegratedExponentialTriangularTransportMap <api-TransportMaps-Maps.html\#TransportMaps.Maps.IntegratedExponentialTriangularTransportMap>`_                        Triangular transport map where each component is represented by an :class:`IntegratedExponential<TransportMaps.MonotonicApproximation.IntegratedExponential>` function.
`CommonBasisIntegratedExponentialTriangularTransportMap <api-TransportMaps-Maps.html\#TransportMaps.Maps.CommonBasisIntegratedExponentialTriangularTransportMap>`_  Triangular transport map :math:`T` where the beases of each component :math:`T_i` are the same for corresponding dimensions.
`IntegratedSquaredTriangularTransportMap <api-TransportMaps-Maps.html\#TransportMaps.Maps.IntegratedSquaredTriangularTransportMap>`_                                Triangular transport map where each component is represented by an :class:`IntegratedSquaredLinearSpanApproximation` function.
`LinearSpanTriangularTransportMap <api-TransportMaps-Maps.html\#TransportMaps.Maps.LinearSpanTriangularTransportMap>`_                                              Triangular transport map where each component is represented by an :class:`FunctionalApproximations.LinearSpanApproximation` function.
`CommonBasisLinearSpanTriangularTransportMap <api-TransportMaps-Maps.html\#TransportMaps.Maps.CommonBasisLinearSpanTriangularTransportMap>`_                        Triangular transport map :math:`T` where the beases of each component :math:`T_i` are the same for corresponding dimensions.
`MonotonicLinearSpanTriangularTransportMap <api-TransportMaps-Maps.html\#TransportMaps.Maps.MonotonicLinearSpanTriangularTransportMap>`_                            Triangular transport map where each component is represented by an :class:`FunctionalApproximations.MonotonicLinearSpanApproximation` function.
`MonotonicCommonBasisLinearSpanTriangularTransportMap <api-TransportMaps-Maps.html\#TransportMaps.Maps.MonotonicCommonBasisLinearSpanTriangularTransportMap>`_      Triangular transport map :math:`T` where the beases of each component :math:`T_i` are the same for corresponding dimensions.
==================================================================================================================================================================  ========================================================================================================================================================================



**Documentation**

.. automodule:: TransportMaps.Maps
   :members:

