TransportMaps.Distributions.Examples.StochasticVolatility
=============================================

**Classes**


.. inheritance-diagram:: TransportMaps.Distributions.Examples.StochasticVolatility.F_phi TransportMaps.Distributions.Examples.StochasticVolatility.F_sigma TransportMaps.Distributions.Examples.StochasticVolatility.IdentityFunction TransportMaps.Distributions.Examples.StochasticVolatility.ConstantFunction TransportMaps.Distributions.Examples.StochasticVolatility.PriorHyperParameters TransportMaps.Distributions.Examples.StochasticVolatility.PriorDynamicsInitialConditions TransportMaps.Distributions.Examples.StochasticVolatility.PriorDynamicsTransition TransportMaps.Distributions.Examples.StochasticVolatility.LogLikelihood TransportMaps.Distributions.Examples.StochasticVolatility.StocVolHyperDistribution
   :parts: 1


================================================================================================================================================================================================  ===============================================================================================================================================
`F_phi <api-TransportMaps-Distributions-Examples-StochasticVolatility.html\#TransportMaps.Distributions.Examples.StochasticVolatility.F_phi>`_
`F_sigma <api-TransportMaps-Distributions-Examples-StochasticVolatility.html\#TransportMaps.Distributions.Examples.StochasticVolatility.F_sigma>`_
`IdentityFunction <api-TransportMaps-Distributions-Examples-StochasticVolatility.html\#TransportMaps.Distributions.Examples.StochasticVolatility.IdentityFunction>`_
`ConstantFunction <api-TransportMaps-Distributions-Examples-StochasticVolatility.html\#TransportMaps.Distributions.Examples.StochasticVolatility.ConstantFunction>`_
`PriorHyperParameters <api-TransportMaps-Distributions-Examples-StochasticVolatility.html\#TransportMaps.Distributions.Examples.StochasticVolatility.PriorHyperParameters>`_                      Distribution :math:`\pi(\mu, \sigma, \phi)`
`PriorDynamicsInitialConditions <api-TransportMaps-Distributions-Examples-StochasticVolatility.html\#TransportMaps.Distributions.Examples.StochasticVolatility.PriorDynamicsInitialConditions>`_  Distribution :math:`g(\mu, \sigma, \phi, {\bf X}_{t_0}) := \pi({\bf X}_{t_0}\vert \mu, \sigma, \phi)`
`PriorDynamicsTransition <api-TransportMaps-Distributions-Examples-StochasticVolatility.html\#TransportMaps.Distributions.Examples.StochasticVolatility.PriorDynamicsTransition>`_                Distribution :math:`f(\mu, \sigma, \phi, {\bf X}_{t_{k}}, {\bf X}_{t_{k+1}}) := \pi({\bf X}_{t_{k+1}}\vert {\bf X}_{t_{k}}, \mu, \sigma, \phi)`
`LogLikelihood <api-TransportMaps-Distributions-Examples-StochasticVolatility.html\#TransportMaps.Distributions.Examples.StochasticVolatility.LogLikelihood>`_                                    Abstract class for log-likelihood :math:`\log \pi({\bf y}_t \vert \mu, \phi, \sigma, {\bf X}_t)`
`StocVolHyperDistribution <api-TransportMaps-Distributions-Examples-StochasticVolatility.html\#TransportMaps.Distributions.Examples.StochasticVolatility.StocVolHyperDistribution>`_
================================================================================================================================================================================================  ===============================================================================================================================================


**Functions**

======================================================================================================================================================================
`generate_data <api-TransportMaps-Distributions-Examples-StochasticVolatility.html\#TransportMaps.Distributions.Examples.StochasticVolatility.generate_data>`_
`trim_distribution <api-TransportMaps-Distributions-Examples-StochasticVolatility.html\#TransportMaps.Distributions.Examples.StochasticVolatility.trim_distribution>`_
======================================================================================================================================================================

**Documentation**

.. automodule:: TransportMaps.Distributions.Examples.StochasticVolatility
   :members:

